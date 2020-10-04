import React, { useState }  from 'react';
import './App.css';
import PhonesGrid from './Components/PhonesGrid/PhonesGrid'
import { Menu } from 'semantic-ui-react'

const App = () => {
  const [navbarState, setNavbarState] = useState({ activeItem: 'home' })

  const handleItemClick = (e, { name }) => setNavbarState({ activeItem: name })

  const { activeItem } = navbarState
  

  return (
    <div className="App" style={{backgroundColor: 'black',color: 'white'}}>
      <Menu inverted>
        <Menu.Item
          name='home'
          active={activeItem === 'home'}
          onClick={handleItemClick}
        />
        <Menu.Item
          name='else'
          active={activeItem === 'else'}
          onClick={handleItemClick}
        />
      </Menu>
      <PhonesGrid/>
    </div>
  );
}

export default App;
