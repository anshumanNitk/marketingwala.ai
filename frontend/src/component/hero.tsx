"use client";

import { ArrowLeft, ChevronDown } from "lucide-react";
import { motion } from "framer-motion";
import {dboss} from "../assets"
import Trypage from "./try";
import { useNavigate } from "react-router-dom";
interface GlassCardProps {
  index: number;
  cardCount: number;
}

const GlassCard: React.FC<GlassCardProps> = ({ index, cardCount }) => {
  const angle = 360 / cardCount; // Spread cards evenly
  const translateZ = 1100; // Increased distance from the center for depth

  return (
    <motion.div
      className="absolute w-[100%] h-[100%] rounded-2xl bg-white bg-opacity-10 backdrop-filter backdrop-blur-lg border border-white border-opacity-20 shadow-xl"
      style={{
        transform: `rotateY(${index * angle}deg) translateZ(${translateZ}px)`,
      }}
    >
    <img 
    src={dboss} // Image source here, can be static or dynamic
    alt="Your description" 
    className="w-[100%] h-[100%] object-cover"
  />
      {/* Reflection or Content */}
    </motion.div>
  );
};

const Carousel3D = () => {
  const cardCount = 10; // Number of cards
  const rotationSpeed = 40; // Speed of rotation

  return (
    <motion.div
      className="relative w-64 h-64 flex justify-center items-center"
      style={{ perspective: 2000 }} // Increased perspective depth for 3D effect
    >
      <motion.div
        className="relative w-full h-full"
        animate={{ rotateY: [0, 360] }} // Continuous rotation
        transition={{
          repeat: Infinity, // Infinite repetition
          ease: "linear", // Smooth linear rotation
          duration: rotationSpeed, // Duration for full rotation
        }}
        style={{
          transformStyle: "preserve-3d", // Preserve 3D transforms
          transformOrigin: "center", // Center rotation
        }}
      >
        {Array.from({ length: cardCount }).map((_, index) => (
          <GlassCard key={index} index={index} cardCount={cardCount} />
        ))}
      </motion.div>
    </motion.div>
  );
};

export default function Landing() {
  const navigate = useNavigate();
  
  const handleOnClick=()=>{
    
    navigate('/dashboard');
  }
  return (
    <div className="min-h-screen text-white flex flex-col items-center justify-center">
      <header className="p-4 flex justify-between items-center w-full">
        <ArrowLeft className="w-6 h-6" />
        <nav className="flex items-center space-x-4">
          <a href="#" className="text-sm hover:text-gray-300 transition-colors">
            Join Us
          </a>
          <a href="#" className="text-sm hover:text-gray-300 transition-colors">
            API
          </a>
          <button className="bg-white text-black px-4 py-2 rounded-full text-sm font-medium hover:bg-opacity-90 transition-colors" onClick={handleOnClick}>
            Try Now
          </button>
        </nav>
      </header>
      <main className="flex-grow flex flex-col items-center justify-center">
        <motion.h1
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-6xl font-serif mb-44 text-center"
        >
          MarketingWala
          <br />
          <span className="font-sans font-bold">One Stop Solution For Social Media Marketing</span>
        </motion.h1>
        <div className="w-full flex justify-center items-center mb-12">
          <Carousel3D />
        </div>
      </main>
      <footer className="pb-4 flex justify-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
        >
          <ChevronDown className="w-6 h-6" />
        </motion.div>
      </footer>
      <Trypage/>
    </div>
  );
}
