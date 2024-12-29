import React from "react";

export default function FilterBlock({filter, filterOptions, selected, setOptions}){

    function updateHandler(option){
        setOptions((prevState)=>({...prevState, [filter]: option}))
    }

    return(
        <article>
            <div>{filter}</div>
            <div><button>{selected}</button></div>
            <div>
                {filterOptions.map((o)=>(
                    <button onClick={()=> updateHandler(o)}>{o}</button>
                ))}
            </div>
        </article>
    )
}