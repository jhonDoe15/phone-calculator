import React from 'react';
import { Card, Icon, Image } from 'semantic-ui-react'

const PhoneCard = (props) => {
    return (
        <Card>
            <Image src={props.imgSrc} size="medium"/>
            <Card.Content>
                <Card.Header>{props.phoneName}</Card.Header>
                <Card.Meta>
                    <span className='date'>Launched in {props.releaseYear}</span>
                </Card.Meta>
                <Card.Description style={{textAlign: 'left'}}>
                    IR: {props.ir}<br/>
                    NFC: {props.nfc}<br/>
                    DUALSIM: {props.dualsim}<br/>
                    3.5mm Jack: {props.jack}<br/>
                    Battery Life: {props.batterylife}<br/>
                    Price: {props.price}<br/>
                    Screen Size: {props.screensize}<br/>
                    Antutu: {props.antutu}<br/>
                    dxomarkScore: {props.dxomarkScore}<br/>
            </Card.Description>
            </Card.Content>
            <Card.Content extra>
                <Icon color="red" name='certificate' />
              {props.score}
        </Card.Content>
        </Card>
    )
}

export default PhoneCard;
