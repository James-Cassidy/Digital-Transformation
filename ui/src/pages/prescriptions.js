
import React , {useState} from 'react';
import Shopping from '../components/Shopping';
import Cart from '../components/Cart';
import '../styles/shopping.css';
import '../styles/cart.css';



const Prescriptions = () => {
	const [show, setShow] = useState(true);
	const [cart , setCart] = useState([]);
	const [warning, setWarning] = useState(false);


const Basket = ({size, setShow}) => {
  return (
    <nav>
        <div className="nav_box" style={{
        display: 'flex',
        justifyContent: 'Center',
        alignItems: 'Left',
        height: '10vh',
        padding: '10px'
      }}>
            <span className="my_shop" onClick={()=>setShow(true)}>
                <h3>Prescriptions&nbsp;&nbsp;</h3>
            </span>
            <div className="cart" onClick={()=>setShow(false)}>
                <span>
                    <i className="fas fa-cart-plus"></i>
                </span>
                <span>{size}</span>
            </div>
        </div>
    </nav>
  )
}

	const handleClick = (item)=>{
		let isPresent = false;
		cart.forEach((product)=>{
			if (item.id === product.id)
			isPresent = true;
		})
		if (isPresent){
			setWarning(true);
			setTimeout(()=>{
				setWarning(false);
			}, 2000);
			return ;
		}
		setCart([...cart, item]);
	}

	const handleChange = (item, d) =>{
		let ind = -1;
		cart.forEach((data, index)=>{
			if (data.id === item.id)
				ind = index;
		});
		const tempArr = cart;
		tempArr[ind].amount += d;
		
		if (tempArr[ind].amount === 0)
			tempArr[ind].amount = 1;
		setCart([...tempArr])
	}

  return (
		<React.Fragment>
		<Basket size={cart.length} setShow={setShow} />
		{
			show ? <Shopping handleClick={handleClick} /> : <Cart cart={cart} setCart={setCart} handleChange={handleChange} />
		}
		{
			warning && <div className='warning'>This prescription has already been added</div>
		}
	</React.Fragment>
  )
}
  
export default Prescriptions;