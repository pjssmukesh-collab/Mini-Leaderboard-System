import React from 'react';
import './Home.css';
import HeroSection from '../components/home/HeroSection';
import BenefitsSection from '../components/home/BenefitsSection';
import EventTypesSection from '../components/home/EventTypesSection';
import CTASection from '../components/home/CTASection';

const Home = () => {
    return (
        <div className="home-page">
            <HeroSection />
            <BenefitsSection />
            <EventTypesSection />
            <CTASection />
        </div>
    );
};

export default Home;
