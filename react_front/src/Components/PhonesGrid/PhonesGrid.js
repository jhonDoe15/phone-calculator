import React, { Fragment, useEffect, useState } from 'react'
import PhoneCard from '../PhoneCard/PhoneCard'
import axios from 'axios';

const PhonesDisplay = (props) => {

    useEffect(() => {
        axios.get("/device/all")
            .then(res => {
                const allDevices = res.data;
                setDevices(allDevices);
            })
        axios.get("/edge-scores")
            .then(res => {
                setEdgeScores(res.data);
            })
    }, []);

    const [devices, setDevices] = useState([]);
    const [edgeScores, setEdgeScores] = useState({});

    const calcScoreForDevice = (antutu, batterylife) => {
        const benchScore = ((antutu - edgeScores.minPerformance) / (edgeScores.topPerformance - edgeScores.minPerformance));//preformance score
        const batteryScore = ((batterylife - edgeScores.minBatteryLife) / (edgeScores.topBatteryLife - edgeScores.minBatteryLife));//battery life score
        const totalScore = (benchScore + batteryScore) / 2 * 100;//Total score without considiration to price
        return totalScore;
    }
    const devicesToShow = devices.sort((b, a) => calcScoreForDevice(a.antutu, a.batterylife) - calcScoreForDevice(b.antutu, b.batterylife))
        .filter(device => device.antutu > 0 && device.batterylife > 0)
        .filter(device => calcScoreForDevice(device.antutu, device.batterylife) > 0)
    const firstColoumn = devicesToShow.filter((device, index) => (parseInt(index) % 3) === 0).map(device => {
        return (
            <PhoneCard key={device.Id} device={device} score={calcScoreForDevice(device.antutu, device.batterylife)} />
        )
    })
    const secondColoumn = devicesToShow.filter((device, index) => (parseInt(index) % 3) === 1).map(device => {
        return (
            <PhoneCard key={device.Id} device={device} score={calcScoreForDevice(device.antutu, device.batterylife)} />
        )
    })
    const thirdColoumn = devicesToShow.filter((device, index) => (parseInt(index) % 3) === 2).map(device => {
        return (
            <PhoneCard key={device.Id} device={device} score={calcScoreForDevice(device.antutu, device.batterylife)} />
        )
    })

    return (
        <Fragment>
            <div className="ui grid">
                <div className="two wide column"></div>
                <div className="four wide column">
                    {firstColoumn}
                </div>
                <div className="four wide column">
                    {secondColoumn}
                </div>
                <div className="four wide column">
                    {thirdColoumn}
                </div>
                <div className="two wide column"></div>
            </div>
        </Fragment>
    )
}


export default PhonesDisplay;