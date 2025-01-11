import React from "react";

export default function CreditInputFilter({filterData, selected, setSelected}){

    function updateHandler(option){
        setSelected((prevState)=>({
            display: {...prevState.display, [filterData.displayText]: option},
            request: {...prevState.request, [filterData.filterId]: filterData.options[option]}
        }))
    }

    return(
        <article>
            {
            <div>
                {filterData.options != null ?(
                    Object.keys(filterData.options).map((o)=>(
                    <button onClick={()=> updateHandler(o)}>{o}</button>
                ))) : null}
            </div>
            }
        </article>
    )
}