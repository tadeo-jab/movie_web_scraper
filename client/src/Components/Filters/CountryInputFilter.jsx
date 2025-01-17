import React, {useRef, useState} from "react";

export default function CountryInputFilter({filterData, selected, setSelected}){

    const inputRef = useRef()
    const [, setRef] = useState('')
    
    const filName = filterData.displayText
    const filId = filterData.filterId
    const filOptions = filterData.options

    function orderSuggestions(item){
        return (item.toLowerCase()).startsWith(inputRef.current?.value.toLowerCase())
    }

    function selectFromDropdown(option){
        if((selected.request?.[filId] !== filOptions[option])){
            inputRef.current.value = option
            setSelected((prevState)=>({
                display: {...prevState.display, [filName]: option},
                request: {...prevState.request, [filId]: filOptions[option]}
            }))
        }  
    }

    function clearInput(){
        inputRef.current.value = ''
        if(filId in selected.request){
            setSelected((prevState)=>{
                const newState = {...prevState}
    
                delete newState.display[filName]
                delete newState.request[filId]
    
                return newState
            })
        }
    }

    //The user can only select a country present in the drop-down list
    //The dropdown is hidden until the user begins typing

    return(
        <article>
            <input ref={inputRef} type="text" maxLength="100" placeholder="Choose a country" onChange={()=>{setRef(inputRef.current.value)}}/>
            <button onClick={()=>clearInput()}>X</button>
            {(inputRef.current?.value !== '') ? (
                <ul>
                    {Object.keys(filOptions).sort().filter(orderSuggestions).map((country)=>(
                        <li onClick={()=>selectFromDropdown(country)}>{country}</li>
                    ))}
                </ul>
            ) : null}
            
        </article>
    )
}