import React from "react";

export default function FilterBlock({filterData, setSelected}){

    function updateHandler(option){
        setSelected((prevState)=>({
            display: {...prevState.display, [filterData['display-name']]: option},
            request: {...prevState.request, [filterData['filter-id']]: filterData.options[option]}
        }))
    }

    return(
        <article>
            <div>{filterData['display-name']}</div>
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