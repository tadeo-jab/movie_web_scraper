import React from "react";

export default function CountryInputFilter({filterData, setSelected}){

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
                    Object.keys(filterData.options).map((o, k)=>(
                    <button onClick={()=> updateHandler(o)} key={k}>{o}</button>
                ))) : null}
            </div>
            }
        </article>
    )
}