import React, { useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { api } from '../../api/client';
import { UploadCloud, CheckCircle, AlertTriangle, ArrowLeft, FileCheck, RefreshCw, BarChart2 } from 'lucide-react';

const UploadFlow = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    
    const [file, setFile] = useState(null);
    const [isUploading, setIsUploading] = useState(false);
    const [uploadRecord, setUploadRecord] = useState(null);
    const [validationReport, setValidationReport] = useState(null);
    const [error, setError] = useState('');
    const [step, setStep] = useState(1); // 1: Upload, 2: Validate/Preview, 3: Process

    const handleFileChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (!file) return;
        setIsUploading(true);
        setError('');
        try {
            const result = await api.uploadResults(id, file);
            setUploadRecord(result);
            setStep(2);
            await handleValidation(result.id);
        } catch (err) {
            setError(err.response?.data?.detail || err.message || 'Upload failed');
        } finally {
            setIsUploading(false);
        }
    };

    const handleValidation = async (uploadId) => {
        try {
            const report = await api.validateUpload(uploadId);
            setValidationReport(report);
        } catch (err) {
            setError(err.response?.data?.detail || err.message || 'Validation failed');
        }
    };

    const handleProcess = async () => {
        setStep(3);
        try {
            if (uploadRecord?.id) {
                await api.processUpload(uploadRecord.id);
            }
        } catch (err) {
            console.error('Failed to process upload:', err);
        }
        setTimeout(() => {
            navigate(`/player/leaderboard/${id}`);
        }, 2000);
    };

    return (
        <div className="py-3" style={{ maxWidth: '840px', margin: '0 auto' }}>
            {/* Navigation back */}
            <div className="mb-4">
                <Link to="/creator/dashboard" className="text-decoration-none text-muted small d-inline-flex align-items-center gap-1 mb-2 hover-primary">
                    <ArrowLeft size={16} /> Back to Dashboard
                </Link>
                <h1 className="h3 fw-bold mb-1">Process Match Results</h1>
                <p className="text-muted small mb-0">
                    Upload tournament match logs, auto-extract player statistics, and calculate scores based on your rule set.
                </p>
            </div>

            {/* Stepper */}
            <div className="step-progress mb-5">
                <div className={`step-item ${step >= 1 ? 'active' : ''} ${step > 1 ? 'completed' : ''}`}>
                    <div className="step-circle">{step > 1 ? '✓' : '1'}</div>
                    <div className="step-label">Upload File</div>
                </div>
                <div className={`step-item ${step >= 2 ? 'active' : ''} ${step > 2 ? 'completed' : ''}`}>
                    <div className="step-circle">{step > 2 ? '✓' : '2'}</div>
                    <div className="step-label">Validate Data</div>
                </div>
                <div className={`step-item ${step >= 3 ? 'active' : ''}`}>
                    <div className="step-circle">3</div>
                    <div className="step-label">Score & Publish</div>
                </div>
            </div>

            {error && <div className="alert alert-danger rounded-3 mb-4">{error}</div>}

            {/* Step 1: Upload */}
            {step === 1 && (
                <div className="card-modern">
                    <div className="card-modern-header">
                        <h2 className="h6 fw-bold mb-0">Upload Tournament Results</h2>
                    </div>
                    <div className="p-4 p-md-5">
                        <div className="dropzone mb-4">
                            <UploadCloud size={44} className="text-primary mb-3" />
                            <h3 className="h6 fw-bold mb-1">Choose Match File to Upload</h3>
                            <p className="text-muted small mb-3">
                                Supports CSV (.csv), Excel (.xlsx), or JSON (.json) data exports
                            </p>
                            
                            <div className="col-md-8 mx-auto">
                                <input 
                                    type="file" 
                                    className="form-control" 
                                    accept=".csv,.xlsx,.json"
                                    onChange={handleFileChange}
                                />
                            </div>

                            {file && (
                                <div className="mt-3 p-2 bg-light border rounded d-inline-flex align-items-center gap-2 small">
                                    <FileCheck size={16} className="text-success" />
                                    <span className="fw-semibold text-dark">{file.name}</span>
                                    <span className="text-muted">({(file.size / 1024).toFixed(1)} KB)</span>
                                </div>
                            )}
                        </div>

                        <div className="d-flex justify-content-between align-items-center pt-3 border-top">
                            <button className="btn btn-outline-secondary px-4" onClick={() => navigate('/creator/dashboard')}>
                                Cancel
                            </button>
                            <button 
                                className="btn btn-primary px-4 py-2" 
                                onClick={handleUpload} 
                                disabled={!file || isUploading}
                            >
                                {isUploading ? (
                                    <>
                                        <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                                        Uploading & Extracting...
                                    </>
                                ) : (
                                    <>
                                        <UploadCloud size={16} className="me-2" /> Upload & Parse Results
                                    </>
                                )}
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Step 2: Error Fallback */}
            {step === 2 && !validationReport && error && (
                <div className="card-modern p-5 text-center my-3">
                    <div className="stat-icon-wrapper stat-icon-amber mx-auto mb-3" style={{ width: '54px', height: '54px' }}>
                        <AlertTriangle size={28} className="text-warning" />
                    </div>
                    <h4 className="fw-bold mb-2">Extraction Could Not Complete</h4>
                    <p className="text-muted small mb-4" style={{ maxWidth: '520px', margin: '0 auto' }}>
                        {error}
                    </p>
                    <button 
                        className="btn btn-primary px-4"
                        onClick={() => {
                            setStep(1);
                            setError('');
                            setFile(null);
                        }}
                    >
                        <ArrowLeft size={16} className="me-1" /> Choose Another File (CSV / Excel / JSON)
                    </button>
                </div>
            )}

            {/* Step 2: Validate & Preview */}
            {step === 2 && validationReport && (
                <div className="card-modern">
                    <div className="card-modern-header d-flex justify-content-between align-items-center">
                        <h2 className="h6 fw-bold mb-0">Validation & Player Verification</h2>
                        <span className="badge-soft-primary">
                            Total Records: {validationReport.total_records}
                        </span>
                    </div>
                    <div className="p-4 p-md-5">
                        <div className="row g-3 text-center mb-4">
                            <div className="col-sm-6 col-md-3">
                                <div className="p-3 rounded-3 border bg-light">
                                    <div className="h3 fw-bold text-success mb-1">{validationReport.valid_records}</div>
                                    <small className="text-muted fw-bold text-uppercase" style={{ fontSize: '0.7rem' }}>Valid Records</small>
                                </div>
                            </div>
                            <div className="col-sm-6 col-md-3">
                                <div className="p-3 rounded-3 border bg-light">
                                    <div className="h3 fw-bold text-warning mb-1">{validationReport.unknown_players}</div>
                                    <small className="text-muted fw-bold text-uppercase" style={{ fontSize: '0.7rem' }}>Unknown Players</small>
                                </div>
                            </div>
                            <div className="col-sm-6 col-md-3">
                                <div className="p-3 rounded-3 border bg-light">
                                    <div className="h3 fw-bold text-danger mb-1">{validationReport.duplicates}</div>
                                    <small className="text-muted fw-bold text-uppercase" style={{ fontSize: '0.7rem' }}>Duplicates</small>
                                </div>
                            </div>
                            <div className="col-sm-6 col-md-3">
                                <div className="p-3 rounded-3 border bg-light">
                                    <div className="h3 fw-bold text-secondary mb-1">{validationReport.invalid_values}</div>
                                    <small className="text-muted fw-bold text-uppercase" style={{ fontSize: '0.7rem' }}>Invalid Values</small>
                                </div>
                            </div>
                        </div>

                        {validationReport.issues && validationReport.issues.length > 0 && (
                            <div className="mb-4">
                                <h3 className="h6 fw-bold text-danger d-flex align-items-center mb-2">
                                    <AlertTriangle size={18} className="me-2"/> Discrepancies Noticed
                                </h3>
                                <div className="border rounded-3 overflow-hidden">
                                    <ul className="list-group list-group-flush small">
                                        {validationReport.issues.map((issue, idx) => (
                                            <li key={idx} className="list-group-item bg-light d-flex justify-content-between align-items-center">
                                                <div>
                                                    <span className="fw-bold text-dark">{issue.issue_type}</span>
                                                    <span className="text-muted ms-2">(Index #{issue.record_index}): {issue.details}</span>
                                                </div>
                                                <span className="badge bg-warning text-dark">Warning</span>
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                        )}

                        <div className="d-flex justify-content-between align-items-center pt-3 border-top">
                            <button className="btn btn-outline-secondary" onClick={() => setStep(1)}>
                                <RefreshCw size={15} className="me-1" /> Re-upload File
                            </button>
                            <button className="btn btn-primary px-4 py-2" onClick={handleProcess}>
                                <CheckCircle size={16} className="me-2" /> Calculate Scores & Finalize
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Step 3: Calculation & Published */}
            {step === 3 && (
                <div className="card-modern p-5 text-center my-3">
                    <div className="spinner-border text-primary mb-3" style={{ width: '3.5rem', height: '3.5rem' }} role="status"></div>
                    <h3 className="h5 fw-bold mb-2">Calculating Official Rankings...</h3>
                    <p className="text-muted small mb-4">
                        Applying dynamic score rules, computing multiplier bonuses, and updating leaderboard.
                    </p>
                    <div className="d-inline-flex flex-column gap-2 text-start p-3 bg-light rounded-3 border">
                        <div className="small d-flex align-items-center text-success"><CheckCircle size={15} className="me-2" /> Match Data Parsed Successfully</div>
                        <div className="small d-flex align-items-center text-success"><CheckCircle size={15} className="me-2" /> Players Mapped to Tournament Roster</div>
                        <div className="small d-flex align-items-center text-success"><CheckCircle size={15} className="me-2" /> Dynamic Scoring Rules Applied</div>
                        <div className="small d-flex align-items-center text-primary"><BarChart2 size={15} className="me-2" /> Redirecting to Live Leaderboard...</div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default UploadFlow;

