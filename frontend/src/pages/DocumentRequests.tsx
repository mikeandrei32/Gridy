import React, { useEffect, useState } from "react"
import { axiosPrivate } from "../api/axios"

interface DocumentRequest {
    id: string;
    document_type: string;
    purpose: string;
    status: string;
    created_at: string;
    user_full_name: string;
}

export const DocumentRequests: React.FC = () => {
    const [requests, setRequests] = useState<DocumentRequest[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchRequests = async () => {
            try {
                const response = await axiosPrivate.get('/services/documents/')
                setRequests(response.data.results || response.data)
            } catch (err) {
                setError('Failed to load document requests.')
                setLoading(false)
            } finally {
              setLoading(false)
            }
        }
        
        fetchRequests();
    }, []);

    const getStatusBadge = (status: string) => {
      switch (status.toLowerCase()) {
        case 'pending':
          return 'bg-yellow-100 text-yellow-800 border-yellow-200'
        case 'approved':
          return 'bg-green-100 text-green-800 border-green-200' 
        case 'rejected':
          return 'bg-red-100 text-red-800 border-red-200';
        default:
          return 'bg-slate-100 text-slate-800 border-slate-200';
      }
    }
  if (loading) return <div className="p-8 text-slate-600">Loading requests...</div>;
  if (error) return <div className="p-8 text-red-600">{error}</div>;
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-slate-900">Document Requests</h2>
        <button className="bg-primary hover:bg-primary-hover text-white px-4 py-2 rounded-md text-sm font-medium transition-colors shadow-sm">
          New Request
        </button>
      </div>
      <div className="bg-surface shadow-sm border border-border rounded-lg overflow-hidden">
        <table className="min-w-full divide-y divide-border">
          <thead className="bg-slate-50">
            <tr>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">ID</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Type</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Purpose</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Date</th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Status</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-border">
            {requests.length === 0 ? (
              <tr>
                <td colSpan={5} className="px-6 py-4 text-center text-sm text-slate-500">No requests found.</td>
              </tr>
            ) : (
              requests.map((req) => (
                <tr key={req.id} className="hover:bg-slate-50 transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-900 font-medium">#{req.id}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-700">{req.document_type}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">{req.purpose}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                    {new Date(req.created_at).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2.5 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full border ${getStatusBadge(req.status)}`}>
                      {req.status}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};