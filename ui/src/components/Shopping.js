import React from 'react';
import list from '../data';
import '../styles/shopping.css';
import Cards from './Cards';

const Shopping = ({handleClick}) => {
  return (
    <section>
        {
            list.map((item)=>(
                <Cards item={item} key={item.id} handleClick={handleClick} />
            ))
        }
    </section>
  )
}
export default Shopping