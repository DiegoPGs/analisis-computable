import { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

const PiApproximationViz = () => {
  const [approximations, setApproximations] = useState([]);
  const [terms, setTerms] = useState(20);

  useEffect(() => {
    // Calcular aproximaciones de π usando la serie de Leibniz
    const calculateApproximations = () => {
      const data = [];
      let sum = 0;
      
      for (let i = 0; i < terms; i++) {
        const term = 4 * (1 / (2 * i + 1)) * (i % 2 ? -1 : 1);
        sum += term;
        data.push({
          terms: i + 1,
          value: sum,
          pi: Math.PI,
          error: Math.abs(sum - Math.PI)
        });
      }
      
      return data;
    };

    setApproximations(calculateApproximations());
  }, [terms]);

  return (
    <div className="p-4 max-w-4xl mx-auto">
      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">
          Número de términos: {terms}
        </label>
        <input
          type="range"
          min="1"
          max="50"
          value={terms}
          onChange={(e) => setTerms(Number(e.target.value))}
          className="w-full"
        />
      </div>

      <div className="border rounded p-4 bg-white">
        <LineChart width={600} height={400} data={approximations}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="terms" 
            label={{ value: 'Número de términos', position: 'bottom' }} 
          />
          <YAxis 
            domain={[2, 4]}
            label={{ value: 'Valor', angle: -90, position: 'left' }} 
          />
          <Tooltip />
          <Line 
            type="monotone" 
            dataKey="value" 
            stroke="#8884d8" 
            name="Aproximación"
          />
          <Line 
            type="monotone" 
            dataKey="pi" 
            stroke="#82ca9d" 
            name="Valor real de π"
            strokeDasharray="5 5"
          />
        </LineChart>
      </div>

      <div className="mt-4 bg-blue-50 p-4 rounded">
        <h3 className="font-medium mb-2">Observaciones:</h3>
        <p>
          La línea azul muestra cómo la aproximación se acerca al valor real de π (línea verde punteada).
          Observe cómo la convergencia es más rápida al principio y luego se hace más lenta.
        </p>
      </div>
    </div>
  );
};

export default PiApproximationViz;
