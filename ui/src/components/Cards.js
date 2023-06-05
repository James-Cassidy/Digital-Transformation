import React from 'react'
import '../styles/cards.css'

const Cards = ({item, handleClick}) => {
  const {title, price, img} = item;
  return (
    <div className="cards">

      <div className="image_box">

        <img src = {img} alt="Prescriptions" />

      </div>

      <div className="details">

        <p>{title}</p>
        <p>Price - £{price}</p>
        <button onClick={()=>handleClick(item)} >Add to Basket</button>

      </div>
    </div>
  )
}

export default Cards