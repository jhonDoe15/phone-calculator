import React, { Fragment } from 'react'
import PhoneCard from '../PhoneCard/PhoneCard'

const PhonesDisplay = (props) => {
    const calcScoreForDevice = (antutu, batterylife) => {
        const benchScore = ((antutu - props.edgeScores.minPerformance) / (props.edgeScores.topPerformance - props.edgeScores.minPerformance));//preformance score
        const batteryScore = ((batterylife - props.edgeScores.minBatteryLife) / (props.edgeScores.topBatteryLife - props.edgeScores.minBatteryLife));//battery life score
        const totalScore = (benchScore + batteryScore) / 2 * 100;//Total score without considiration to price
        return totalScore;
    }
    const devicesToShow = props.devices.sort((b, a) => calcScoreForDevice(a.antutu, a.batterylife) - calcScoreForDevice(b.antutu, b.batterylife))
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