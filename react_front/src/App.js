import React, { useEffect, useState } from 'react';
import './App.css';
import PhoneCard from './Components/PhoneCard/PhoneCard'
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
  });

  const [devices, setDevices] = useState([]);
  const [edgeScores, setEdgeScores] = useState(
    {
      minPerformance: 0,
      topPerformance: 0,
      minBatteryLife: 0,
      topBatteryLife: 0,
      minScreenSize: 0,
      topScreenSize: 0,
    }
  );

  const calcScoreForDevice = (antutu, screen_size, year, batterylife) => {
    const benchScore = ((antutu - edgeScores.minPerformance) / (edgeScores.topPerformance - edgeScores.minPerformance));//preformance score
    const batteryScore = ((batterylife - edgeScores.minBatteryLife) / (edgeScores.topBatteryLife - edgeScores.minBatteryLife));//battery life score
    const screenScore = ((screen_size - edgeScores.minScreenSize) / (edgeScores.topScreenSize - edgeScores.minScreenSize));//screen size score
    const totalScore = (benchScore + batteryScore + screenScore) / 3 * 100;//Total score without considiration to price
    return totalScore;
  }
  const devicesToShow = devices.map(device => {
    return (
      <PhoneCard
        phoneName={device.devicename}
        imgSrc={device.ImageURL}
        releaseYear={device.year}
        ir={device.ir}
        nfc={device.nfc}
        antut={device.antutu}
        dxomarkScore={device.dxomarkScore}
        screensize={device.screensize}
        jack={device.headphonejack}
        batterylife={device.batterylife}
      /*{ score={() => calcScoreForDevice(device.price, device.antutu, device.screensize, device.year, device.batterylife)}}*/
      />
    )
  })

  return (
    <div className="App">
      <div class="ui grid">
        <div class="six wide column"></div>
        <div class="four wide column">
          {devicesToShow}
        </div>
        <div class="six wide column"></div>
      </div>

    </div>
  );
}

export default App;
