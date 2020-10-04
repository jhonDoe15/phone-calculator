import React from 'react';
import { Card, Icon, Image } from 'semantic-ui-react'

const PhoneCard = (props) => {

    const getTwoDecimalPoints = (score) => {
        if (score) {
           return score.toFixed(3); 
        }
        return score;
    }

    return (
        <Card>
            <Image src={props.device.ImageURL} size="small" className="centered" style={{backgroundColor: 'black', color: 'white'}} />
            <Card.Content style={{backgroundColor: 'black', color: 'white'}}>
                <Card.Header style={{backgroundColor: 'black', color: 'white'}}>{props.device.devicename}</Card.Header>
                <Card.Meta style={{backgroundColor: 'black', color: 'white'}}>
                    <span className='date'>Launched in {props.device.year}</span>
                </Card.Meta>
                <Card.Description style={{ textAlign: 'left', fontSize: '1vw',backgroundColor: 'black', color: 'white' }}>
                    IR: {props.device.ir === "1" ? "True" : "False"}<br />
                    NFC: {props.device.nfc === "1" ? "True" : "False"}<br />
                    DUALSIM: {props.device.dualsim === "1" ? "True" : "False"}<br />
                    3.5mm Jack: {props.device.headphonejack === "1" ? "True" : "False"}<br />
                    Battery Life: {props.device.batterylife}<br />
                    Price: {props.device.price}$<br />
                    Screen Size: {props.device.screensize}<br />
                    Antutu: {props.device.antutu}<br />
                    dxomarkScore: {props.device.dxomarkScore}<br />
                </Card.Description>
            </Card.Content>
            <Card.Content extra style={{backgroundColor: 'black', color: 'white'}}>
                <Icon color="red" name='certificate' />
                {getTwoDecimalPoints(props.score)}
            </Card.Content>
        </Card>
    )
}

export default PhoneCard;
