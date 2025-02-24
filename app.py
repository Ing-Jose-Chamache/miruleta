import React, { useState } from 'react';

const RuletaPreviewFinal = () => {
  const [rotation, setRotation] = useState(0);
  const [nombres, setNombres] = useState(["TUPIA", "ALVITES", "CHAVEZ", "ESPINOZA", "TORRES"]);
  const [textAreaValue, setTextAreaValue] = useState(nombres.join('\n'));
  const [ganador, setGanador] = useState('');
  const [isSpinning, setIsSpinning] = useState(false);
  const [indicadorAngulo, setIndicadorAngulo] = useState(null);
  
  const colors = ['#FF9999', '#99FF99', '#9999FF', '#FFFF99', '#FF99FF'];
  const anglePerSection = 360 / nombres.length;
  
  const handleSpin = () => {
    if (isSpinning) return;
    
    setIsSpinning(true);
    setGanador('');
    setIndicadorAngulo(null);
    const newRotation = rotation + 1440 + Math.random() * 360;
    setRotation(newRotation);
    
    setTimeout(() => {
      const finalAngle = newRotation % 360;
      const winnerIndex = Math.floor(finalAngle / anglePerSection);
      setGanador(nombres[winnerIndex % nombres.length]);
      setIndicadorAngulo(finalAngle + (anglePerSection / 2));
      setIsSpinning(false);
    }, 4000);
  };

  const handleTextChange = (e) => {
    setTextAreaValue(e.target.value);
  };

  const handleLoadNames = () => {
    const newNames = textAreaValue
      .split('\n')
      .map(name => name.trim())
      .filter(name => name.length > 0);
    if (newNames.length > 0) {
      setNombres(newNames);
      setGanador('');
      setIndicadorAngulo(null);
    }
  };

  const renderWinnerArrow = () => {
    if (!indicadorAngulo || isSpinning) return null;

    // Dimensiones reducidas de la flecha (50% del tamaño original)
    const arrowLength = 20;
    const arrowWidth = 10;
    const centerX = 50;
    const centerY = 50;
    const radius = 45;
    
    const angle = (indicadorAngulo - 90) * (Math.PI / 180);
    const tipX = centerX + (radius + 5) * Math.cos(angle);
    const tipY = centerY + (radius + 5) * Math.sin(angle);
    
    const baseAngle = angle + Math.PI;
    const baseX = tipX + arrowLength * Math.cos(baseAngle);
    const baseY = tipY + arrowLength * Math.sin(baseAngle);
    
    const leftX = tipX + arrowWidth * Math.cos(baseAngle + Math.PI/2);
    const leftY = tipY + arrowWidth * Math.sin(baseAngle + Math.PI/2);
    const rightX = tipX + arrowWidth * Math.cos(baseAngle - Math.PI/2);
    const rightY = tipY + arrowWidth * Math.sin(baseAngle - Math.PI/2);

    return (
      <polygon
        points={`${tipX},${tipY} ${leftX},${leftY} ${baseX},${baseY} ${rightX},${rightY}`}
        fill="gold"
        stroke="darkgolden"
        strokeWidth="0.5"
      />
    );
  };

  return (
    <div className="flex flex-row gap-4 p-4 bg-gray-100 rounded-lg">
      {/* Panel izquierdo */}
      <div className="flex flex-col bg-white p-4 rounded shadow">
        <label className="text-sm font-semibold mb-2">Lista de Nombres:</label>
        <textarea 
          className="border p-2 h-64 w-48 mb-2 font-mono text-sm"
          value={textAreaValue}
          onChange={handleTextChange}
          placeholder="Ingrese nombres aquí, uno por línea"
        />
        <button 
          onClick={handleLoadNames}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Cargar Nombres
        </button>
      </div>

      {/* Panel derecho - Ruleta */}
      <div className="flex flex-col items-center bg-white p-4 rounded shadow">
        <div className="relative w-80 h-80">
          {/* Ruleta */}
          <svg 
            className="w-full h-full"
            viewBox="0 0 100 100"
            style={{
              transform: `rotate(${rotation}deg)`,
              transition: 'transform 4s cubic-bezier(0.2, 0.8, 0.2, 1)'
            }}
          >
            {nombres.map((nombre, index) => {
              const startAngle = index * anglePerSection;
              const endAngle = (index + 1) * anglePerSection;
              
              const startRad = (startAngle - 90) * Math.PI / 180;
              const endRad = (endAngle - 90) * Math.PI / 180;
              
              const startX = 50 + 45 * Math.cos(startRad);
              const startY = 50 + 45 * Math.sin(startRad);
              const endX = 50 + 45 * Math.cos(endRad);
              const endY = 50 + 45 * Math.sin(endRad);
              
              const largeArcFlag = anglePerSection <= 180 ? 0 : 1;
              
              const pathData = `
                M 50 50
                L ${startX} ${startY}
                A 45 45 0 ${largeArcFlag} 1 ${endX} ${endY}
                Z
              `;
              
              const textAngle = (startAngle + endAngle) / 2;
              const textRad = (textAngle - 90) * Math.PI / 180;
              const textX = 50 + 30 * Math.cos(textRad);
              const textY = 50 + 30 * Math.sin(textRad);
              
              return (
                <g key={index}>
                  <path
                    d={pathData}
                    fill={colors[index % colors.length]}
                    stroke="white"
                    strokeWidth="0.5"
                  />
                  <text
                    x={textX}
                    y={textY}
                    fontSize="6"
                    fill="black"
                    textAnchor="middle"
                    transform={`rotate(${textAngle}, ${textX}, ${textY})`}
                  >
                    {nombre}
                  </text>
                </g>
              );
            })}
            {/* Círculo central */}
            <circle cx="50" cy="50" r="5" fill="white" stroke="black" />
            
            {/* Flecha ganadora */}
            {renderWinnerArrow()}
          </svg>
          
          {/* Flecha indicadora fija */}
          <div className="absolute right-0 top-1/2 -mt-2 w-0 h-0 
                        border-t-8 border-t-transparent
                        border-l-[16px] border-l-red-600
                        border-b-8 border-b-transparent">
          </div>
        </div>
        
        {/* Botón de giro y resultado */}
        <button 
          onClick={handleSpin}
          disabled={isSpinning}
          className={`mt-4 px-6 py-2 rounded text-white transition-colors ${
            isSpinning ? 'bg-gray-400' : 'bg-blue-500 hover:bg-blue-600'
          }`}
        >
          {isSpinning ? 'Girando...' : 'Girar Ruleta'}
        </button>
        
        {ganador && (
          <div className="mt-4 text-center">
            <h3 className="text-xl font-bold">¡GANADOR!</h3>
            <p className="text-2xl font-bold text-blue-600">{ganador}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default RuletaPreviewFinal;