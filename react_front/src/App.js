import React, { useEffect, useState } from 'react';
import './App.css';
import PhonesDisplay from './Components/PhonesDisplay/PhonesDisplay'
import axios from 'axios';

const App = () => {

  useEffect(() => {
    axios.get("http://127.0.0.1:5000/device/all")
      .then(res => {
        const allDevices = res.data;
        setDevices(allDevices);
      })
    axios.get("http://127.0.0.1:5000/edge-scores")
      .then(res => {
        setEdgeScores(res.data);
      })
  },[]);

  const [devices, setDevices] = useState([]);
  const [edgeScores, setEdgeScores] = useState(
    {
      
    }
  );

  return (
    <div className="App">
      <PhonesDisplay devices={devices} edgeScores={edgeScores}/>
    </div>
  );
}

export default App;
