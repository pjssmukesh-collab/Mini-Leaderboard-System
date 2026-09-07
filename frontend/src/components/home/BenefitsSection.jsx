import React from 'react';
import { Settings, UploadCloud, BarChart2 } from 'lucide-react';

const BenefitsSection = () => {
    return (
        <section id="features" className="section-padding">
            <div className="container">
                <div className="text-center mb-5 pb-3">
                    <h2 className="display-5 fw-bold mb-3">Less manual work.<br/>More meaningful rankings.</h2>
                    <p className="lead text-muted mx-auto" style={{ maxWidth: '600px' }}>
                        Our platform abstracts away the complexity of managing leaderboards, so you can focus on the event.
                    </p>
                </div>
                <div className="row g-4">
                    <div className="col-md-4">
                        <div className="card-premium p-4 p-xl-5">
                            <div className="icon-box">
                                <Settings size={24} />
                            </div>
                            <h4 className="fw-bold mb-3">Configure Once</h4>
                            <p className="text-muted mb-0">
                                Define your scoring rules, participant groups, and ranking formulas just once. Re-use them across multiple seasons or events.
                            </p>
                        </div>
                    </div>
                    <div className="col-md-4">
                        <div className="card-premium p-4 p-xl-5">
                            <div className="icon-box">
                                <UploadCloud size={24} />
                            </div>
                            <h4 className="fw-bold mb-3">Upload Easily</h4>
                            <p className="text-muted mb-0">
                                Drag and drop CSVs, connect via API, or enter results manually. We handle the data ingestion and validation for you.
                            </p>
                        </div>
                    </div>
                    <div className="col-md-4">
                        <div className="card-premium p-4 p-xl-5">
                            <div className="icon-box">
                                <BarChart2 size={24} />
                            </div>
                            <h4 className="fw-bold mb-3">Rank Automatically</h4>
                            <p className="text-muted mb-0">
                                Our engine calculates the standings in real-time. Publish beautiful leaderboards instantly without writing a line of code.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default BenefitsSection;
