"use client";

import { ArrowLeft, ChevronDown } from "lucide-react";
import { dboss } from "../assets";
import Trypage from "./try";
import { useNavigate } from "react-router-dom";

interface GlassCardProps {
  index: number;
  cardCount: number;
}

const GlassCard: React.FC<GlassCardProps> = ({ index, cardCount }) => {
  const angle = 360 / cardCount;
  const translateZ = 1100;

  return (
    <div
      className="absolute w-[100%] h-[100%] rounded-2xl bg-transparent backdrop-filter backdrop-blur-lg border border-white border-opacity-20 shadow-xl"
      style={{
        transform: `rotateY(${index * angle}deg) translateZ(${translateZ}px)`,
      }}
    >
      <img 
        src={dboss} 
        alt="Description" 
        className="w-[100%] h-[100%] object-cover"
      />
    </div>
  );
};

const Carousel3D = () => {
  const cardCount = 10;

  return (
    <div className="relative w-64 h-64 flex justify-center items-center" style={{ perspective: 2000 }}>
      <div
        className="relative w-full h-full"
        style={{
          transformStyle: "preserve-3d",
          transformOrigin: "center",
        }}
      >
        {Array.from({ length: cardCount }).map((_, index) => (
          <GlassCard key={index} index={index} cardCount={cardCount} />
        ))}
      </div>
    </div>
  );
};

export default function Landing() {
  const navigate = useNavigate();
  
  const handleOnClick = () => {
    navigate("/dashboard");
  };

  return (
    <div className="min-h-screen text-white flex flex-col items-center justify-center">
      <header className="p-4 flex justify-between items-center w-full">
        <ArrowLeft className="w-6 h-6" />
        <nav className="flex items-center space-x-4">
          <a href="#" className="text-sm hover:text-gray-300 transition-colors">Join Us</a>
          <a href="#" className="text-sm hover:text-gray-300 transition-colors">API</a>
          <button 
            className="bg-white text-black px-4 py-2 rounded-full text-sm font-medium hover:bg-opacity-90 transition-colors" 
            onClick={handleOnClick}
          >
            Try Now
          </button>
        </nav>
      </header>
      <main className="flex-grow flex flex-col items-center justify-center">
        <h1 className="text-6xl font-serif mb-44 text-center">
          MarketingWala
          <br />
          <span className="font-sans font-bold">One Stop Solution For Social Media Marketing</span>
        </h1>
        <div className="w-full flex justify-center items-center mb-12">
          <Carousel3D />
        </div>
      </main>
      <footer className="pb-4 flex justify-center">
        <ChevronDown className="w-6 h-6" />
      </footer>
      <Trypage />
    </div>
  );
}
