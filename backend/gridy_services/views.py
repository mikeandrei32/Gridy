from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

from gridy_auth.models import User
from gridy_auth.permissions import IsBarangayOfficial
from .models import DocumentRequest, QueueTicket
from .serializers import DocumentRequestSerializer, QueueTicketSerializer
from gridy_communications.services import send_notification_to_user


class DocumentRequestViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.ADMIN:
            return DocumentRequest.objects.all().order_by('-created_at')
        return DocumentRequest.objects.filter(user=user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['patch'], permission_classes=[IsBarangayOfficial])
    def validate(self, request, pk=None):
        document_request = self.get_object()
        new_status = request.data.get('status')
        admin_notes = request.data.get('admin_notes', '')

        # Enforce valid transition states
        if new_status not in [DocumentRequest.Status.APPROVED, DocumentRequest.Status.REJECTED, DocumentRequest.Status.RELEASED]:
            return Response(
                {"detail": "Invalid status transition."},
                status=status.HTTP_400_BAD_REQUEST
            )

        document_request.status = new_status
        if admin_notes:
            document_request.admin_notes = admin_notes
        document_request.save()

        # Trigger push notification to the resident
        send_notification_to_user(
            user=document_request.user,
            title="Document Request Update",
            body=f"Your request for {document_request.document_type} is now {document_request.get_status_display()}.",
            data={"request_id": str(document_request.id)}
        )
        
        return Response(DocumentRequestSerializer(document_request).data, status=status.HTTP_200_OK)


class QueueTicketViewSet(viewsets.ModelViewSet):
    queryset = QueueTicket.objects.all()
    serializer_class = QueueTicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user if self.request.user.is_authenticated else None)

    @action(detail=False, methods=['get'], url_path='live-status')
    def live_status(self, request):
        serving_ticket = QueueTicket.objects.filter(status=QueueTicket.Status.SERVING).first()
        total_waiting = QueueTicket.objects.filter(status=QueueTicket.Status.WAITING).count()
        
        return Response({
            "current_ticket": serving_ticket.ticket_number if serving_ticket else None,
            "total_waiting": total_waiting,
            "avg_wait_mins": total_waiting * 2 
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='next', permission_classes=[IsBarangayOfficial])
    def next_ticket(self, request):
        with transaction.atomic():
            QueueTicket.objects.filter(status=QueueTicket.Status.SERVING).update(status=QueueTicket.Status.COMPLETED)
            
            next_ticket = QueueTicket.objects.filter(status=QueueTicket.Status.WAITING).order_by('created_at').first()
            
            if not next_ticket:
                return Response(
                    {"detail": "No tickets waiting in queue."},
                    status=status.HTTP_404_NOT_FOUND
                )
                
            next_ticket.status = QueueTicket.Status.SERVING
            next_ticket.save()

            # Trigger push notification if the ticket is linked toa regsitered resident

            if next_ticket.user:
                send_notification_to_user(
                    user=next_ticket.user,
                    title="Queue Update",
                    body=f"Your ticket {next_ticket.ticket_number} is now being served!",
                    data={"ticket_id": str(next_ticket.id)}
                )
            
            remaining_waiting = QueueTicket.objects.filter(status=QueueTicket.Status.WAITING).count()
            
            return Response({
                "current_ticket": next_ticket.ticket_number,
                "remaining_waiting": remaining_waiting
            }, status=status.HTTP_200_OK)
