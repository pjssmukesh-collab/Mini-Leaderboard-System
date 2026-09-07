import React from 'react';
import { Upload, FileText, FileSpreadsheet, Image, Code } from 'lucide-react';

const fileTypes = [
    { icon: Image, label: 'Photo' },
    { icon: FileText, label: 'CSV' },
    { icon: FileSpreadsheet, label: 'Excel' },
    { icon: Code, label: 'JSON' },
];

const UploadSection = () => {
    return (
        <section id="how-it-works" style={{ padding: '6rem 0' }}>
            <div className="container">
                <div className="row align-items-center">
                    <div className="col-lg-6 mb-5 mb-lg-0">
                        <span style={{
                            fontSize: '0.75rem',
                            textTransform: 'uppercase',
                            letterSpacing: '2px',
                            color: '#888',
                            fontWeight: 600,
                            display: 'block',
                            marginBottom: '1rem',
                        }}>
                            Automated Result Processing
                        </span>
                        <h2 style={{
                            fontFamily: "'Playfair Display', serif",
                            fontSize: '3rem',
                            fontWeight: 700,
                            lineHeight: 1.15,
                            marginBottom: '1rem',
                        }}>
                            Upload the result.<br />
                            Let the system do the work.
                        </h2>
                        <p style={{ color: '#666', fontSize: '1rem', maxWidth: '500px' }}>
                            Support for images, CSV, Excel, JSON with OCR-powered extraction.
                        </p>
                    </div>
                    <div className="col-lg-6">
                        <div style={{
                            background: '#fff',
                            border: '2px dashed #d0d0d0',
                            borderRadius: '16px',
                            padding: '3rem 2rem',
                            textAlign: 'center',
                        }}>
                            <div style={{
                                width: '60px',
                                height: '60px',
                                borderRadius: '50%',
                                backgroundColor: '#f0f4ed',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                margin: '0 auto 1.5rem',
                                color: '#4a5d23',
                            }}>
                                <Upload size={28} />
                            </div>
                            <h5 style={{ fontWeight: 600, marginBottom: '0.25rem' }}>
                                Drop your event result here
                            </h5>
                            <p style={{ color: '#999', fontSize: '0.9rem', marginBottom: '2rem' }}>
                                or click to browse
                            </p>

                            <div className="d-flex justify-content-center gap-2 flex-wrap mb-4">
                                {fileTypes.map((ft, i) => (
                                    <div key={i} style={{
                                        border: '1px solid #e0e0e0',
                                        borderRadius: '8px',
                                        padding: '0.5rem 1rem',
                                        display: 'flex',
                                        alignItems: 'center',
                                        gap: '0.5rem',
                                        fontSize: '0.85rem',
                                        color: '#555',
                                    }}>
                                        <ft.icon size={16} />
                                        {ft.label}
                                    </div>
                                ))}
                            </div>

                            <button style={{
                                backgroundColor: '#4a5d23',
                                color: '#fff',
                                border: 'none',
                                borderRadius: '50px',
                                padding: '0.7rem 2rem',
                                fontWeight: 500,
                                cursor: 'pointer',
                                transition: 'background-color 0.2s',
                            }}>
                                Upload Result
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default UploadSection;
