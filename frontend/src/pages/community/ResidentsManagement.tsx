import toast from 'react-hot-toast';
import React, { useEffect, useState } from "react";
import { axiosPrivate } from "../../api/axios";
import { Search, Trash2, Mail, Phone, Upload, Download, FileSpreadsheet, X, CheckCircle2, AlertCircle } from "lucide-react";

interface Resident {
    id: number;
    username?: string;
    email?: string;
    full_name: string;
    birth_date: string;
    voter_status: boolean;
    contact_number: string;
    purok?: string | number | null;
}

interface ImportSummary {
    imported: number;
    skipped_due_to_duplicate: number;
    errors: string[];
}

export const ResidentsManagement: React.FC = () => {
    const [residents, setResidents] = useState<Resident[]>([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState('');

    // Import Modal State
    const [isImportModalOpen, setIsImportModalOpen] = useState(false);
    const [csvFile, setCsvFile] = useState<File | null>(null);
    const [importing, setImporting] = useState(false);
    const [importSummary, setImportSummary] = useState<ImportSummary | null>(null);

    const fetchResidents = async () => {
        try {
            const response = await axiosPrivate.get('/auth/resident/');
            setResidents(response.data.results || response.data);
        } catch (err) {
            console.error("Failed to fetch directory:", err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchResidents();
    }, []);

    const handleDelete = async (id: number) => {
        if (!window.confirm("Are you sure you want to permanently remove this resident? This will revoke all their access.")) return;
        try {
            await axiosPrivate.delete(`/auth/resident/${id}/`);
            setResidents(prev => prev.filter(r => r.id !== id));
            toast.success('Resident record deleted.');
        } catch (err) {
            console.error("Failed to delete resident", err);
            toast.error('Failed to delete resident.');
        }
    };

    const handleDownloadTemplate = () => {
        const header = "username,email,full_name,birth_date,contact_number,purok,voter_status\n";
        const sample1 = "juandelacruz,juan@example.com,Juan Dela Cruz,1990-05-15,09171234567,Purok Maligaya,True\n";
        const sample2 = "mariasantos,,Maria Santos,1985-11-20,,Purok 2,False\n";
        const csvContent = "data:text/csv;charset=utf-8," + header + sample1 + sample2;
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "barangay_rbi_template.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            if (!file.name.endsWith('.csv')) {
                toast.error('Please upload a valid .csv file.');
                return;
            }
            setCsvFile(file);
            setImportSummary(null);
        }
    };

    const handleImportSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!csvFile) {
            toast.error('Please select a CSV file to import.');
            return;
        }

        try {
            setImporting(true);
            const formData = new FormData();
            formData.append('file', csvFile);

            const res = await axiosPrivate.post('/auth/import-residents/', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });

            setImportSummary(res.data);
            toast.success(`Successfully imported ${res.data.imported} resident records!`);
            fetchResidents();
        } catch (err: any) {
            const errorData = err.response?.data;
            if (errorData && errorData.imported !== undefined) {
                setImportSummary(errorData);
                toast.error('Import completed with validation warnings.');
                fetchResidents();
            } else {
                toast.error(errorData?.detail || 'Failed to import CSV file.');
            }
        } finally {
            setImporting(false);
        }
    };

    const filteredResidents = residents.filter(r => 
        (r.full_name || '').toLowerCase().includes(search.toLowerCase()) || 
        (r.username || '').toLowerCase().includes(search.toLowerCase()) ||
        String(r.purok || '').toLowerCase().includes(search.toLowerCase())
    );

    return (
        <div className="space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <div>
                    <h1 className="text-2xl font-extrabold text-[#0f172a] tracking-tight">Residents Directory & RBI</h1>
                    <p className="text-[#64748b] text-sm mt-1">Manage verified residents and import census rosters.</p>
                </div>
                
                <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
                    <div className="relative max-w-sm w-full">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                        <input
                            type="text"
                            placeholder="Search name, ID, or purok..."
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                            className="w-full pl-10 pr-4 py-2 bg-white border border-slate-200 rounded-xl text-sm focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all shadow-sm"
                        />
                    </div>

                    <button
                        onClick={() => {
                            setIsImportModalOpen(true);
                            setImportSummary(null);
                            setCsvFile(null);
                        }}
                        className="inline-flex items-center justify-center gap-2 px-4 py-2 bg-[#0047BA] hover:bg-[#003882] text-white rounded-xl text-sm font-bold shadow-sm transition-all cursor-pointer shrink-0"
                    >
                        <Upload className="w-4 h-4" />
                        <span>Import CSV</span>
                    </button>
                </div>
            </div>

            <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
                <div className="overflow-x-auto">
                    <table className="w-full text-left text-sm">
                        <thead>
                            <tr className="bg-slate-50 text-[#64748b] text-[11px] font-bold uppercase tracking-wider border-b border-slate-100">
                                <th className="py-3.5 px-6">Resident Info</th>
                                <th className="py-3.5 px-6">Purok / Zone</th>
                                <th className="py-3.5 px-6">Account ID</th>
                                <th className="py-3.5 px-6">Contact</th>
                                <th className="py-3.5 px-6 text-center">Voter Status</th>
                                <th className="py-3.5 px-6 text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                            {loading ? (
                                <tr><td colSpan={6} className="py-12 text-center text-slate-400">Loading directory...</td></tr>
                            ) : filteredResidents.length === 0 ? (
                                <tr><td colSpan={6} className="py-12 text-center text-slate-400">No verified residents found.</td></tr>
                            ) : (
                                filteredResidents.map(resident => (
                                    <tr key={resident.id} className="hover:bg-slate-50/50 transition-colors">
                                        <td className="py-3 px-6">
                                            <div className="flex items-center gap-3">
                                                <div className="w-9 h-9 rounded-full bg-blue-50 text-blue-600 flex items-center justify-center font-bold">
                                                    {resident.full_name.charAt(0).toUpperCase()}
                                                </div>
                                                <div>
                                                    <div className="font-bold text-slate-900">{resident.full_name}</div>
                                                    <div className="text-xs text-slate-500">Born: {resident.birth_date}</div>
                                                </div>
                                            </div>
                                        </td>
                                        <td className="py-3 px-6 font-medium text-slate-700">
                                            {resident.purok ? String(resident.purok) : <span className="text-slate-400 italic">Unassigned</span>}
                                        </td>
                                        <td className="py-3 px-6 text-slate-600 font-mono text-xs">
                                            {resident.username || 'None'}
                                        </td>
                                        <td className="py-3 px-6 text-slate-600">
                                            <div className="flex flex-col gap-0.5 text-xs">
                                                {resident.contact_number && (
                                                    <span className="flex items-center gap-1.5"><Phone className="w-3 h-3 text-slate-400" /> {resident.contact_number}</span>
                                                )}
                                                {resident.email && (
                                                    <span className="flex items-center gap-1.5"><Mail className="w-3 h-3 text-slate-400" /> {resident.email}</span>
                                                )}
                                                {!resident.contact_number && !resident.email && <span className="text-slate-400 italic">No contact info</span>}
                                            </div>
                                        </td>
                                        <td className="py-3 px-6 text-center">
                                            {resident.voter_status ? (
                                                <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
                                                    Registered Voter
                                                </span>
                                            ) : (
                                                <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-slate-50 text-slate-500 border border-slate-200">
                                                    Non-Voter
                                                </span>
                                            )}
                                        </td>
                                        <td className="py-3 px-6 text-right">
                                            <button
                                                onClick={() => handleDelete(resident.id)}
                                                title="Delete Resident"
                                                className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors cursor-pointer"
                                            >
                                                <Trash2 className="w-4 h-4" />
                                            </button>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* CSV Import Modal */}
            {isImportModalOpen && (
                <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs">
                    <div className="bg-white rounded-2xl shadow-2xl max-w-lg w-full overflow-hidden animate-in fade-in zoom-in-95">
                        <div className="px-6 py-5 border-b border-slate-100 flex justify-between items-center bg-slate-50">
                            <div className="flex items-center gap-2.5">
                                <FileSpreadsheet className="w-5 h-5 text-[#0047BA]" />
                                <h3 className="text-base font-bold text-slate-900">Import Census / RBI Records</h3>
                            </div>
                            <button
                                onClick={() => setIsImportModalOpen(false)}
                                className="text-slate-400 hover:text-slate-600 rounded-lg p-1 transition-colors"
                            >
                                <X className="w-5 h-5" />
                            </button>
                        </div>

                        <form onSubmit={handleImportSubmit} className="p-6 space-y-5">
                            <div className="flex items-center justify-between p-3.5 bg-blue-50/70 border border-blue-100 rounded-xl">
                                <div className="text-xs text-slate-700">
                                    <span className="font-bold block">Need the standard format?</span>
                                    Download the pre-structured RBI template.
                                </div>
                                <button
                                    type="button"
                                    onClick={handleDownloadTemplate}
                                    className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white hover:bg-blue-50 border border-blue-200 text-blue-700 text-xs font-bold rounded-lg shadow-2xs transition-colors shrink-0 cursor-pointer"
                                >
                                    <Download className="w-3.5 h-3.5" />
                                    <span>Download Template</span>
                                </button>
                            </div>

                            <div>
                                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
                                    Upload CSV File (.csv)
                                </label>
                                <input
                                    type="file"
                                    accept=".csv"
                                    onChange={handleFileChange}
                                    className="w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-bold file:bg-slate-100 file:text-slate-700 hover:file:bg-slate-200 cursor-pointer border border-slate-200 rounded-xl p-2 bg-slate-50/50"
                                />
                                <p className="text-[11px] text-slate-400 mt-1">
                                    File must include columns: <code>username, full_name, birth_date, purok, voter_status</code>.
                                </p>
                            </div>

                            {/* Summary Report */}
                            {importSummary && (
                                <div className="p-4 rounded-xl border border-slate-200 bg-slate-50 space-y-2">
                                    <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider">Import Report</h4>
                                    <div className="flex items-center gap-4 text-xs font-semibold">
                                        <span className="flex items-center gap-1 text-emerald-600">
                                            <CheckCircle2 className="w-3.5 h-3.5" /> {importSummary.imported} Imported
                                        </span>
                                        <span className="text-slate-500">
                                            {importSummary.skipped_due_to_duplicate} Skipped (Duplicates)
                                        </span>
                                    </div>
                                    {importSummary.errors.length > 0 && (
                                        <div className="mt-2 text-xs text-rose-600 max-h-24 overflow-y-auto space-y-1">
                                            {importSummary.errors.map((err, i) => (
                                                <div key={i} className="flex items-start gap-1">
                                                    <AlertCircle className="w-3 h-3 shrink-0 mt-0.5" />
                                                    <span>{err}</span>
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            )}

                            <div className="pt-2 flex items-center justify-end gap-3">
                                <button
                                    type="button"
                                    onClick={() => setIsImportModalOpen(false)}
                                    className="px-4 py-2 text-sm font-semibold text-slate-600 hover:text-slate-800 rounded-xl transition-colors"
                                >
                                    Close
                                </button>
                                <button
                                    type="submit"
                                    disabled={importing || !csvFile}
                                    className="px-5 py-2 text-sm font-bold text-white bg-[#0047BA] hover:bg-[#003882] rounded-xl transition-all shadow-md shadow-blue-500/20 disabled:opacity-50 cursor-pointer"
                                >
                                    {importing ? 'Importing Census...' : 'Start Import'}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};