import React from "react";
import MultiSelectFilter from "./Filters/MultiSelectFilter.jsx";
import SingleSelectFilter from "./Filters/SingleSelectFilter.jsx";
import RangeSliderFilter from "./Filters/RangeSliderFilter.jsx";
import CreditInputFilter from "./Filters/CreditInputFilter.jsx";
import CountryInputFilter from "./Filters/CountryInputFilter.jsx";

export default function FilterBlock({filterData, setSelected}){

    function updateHandler(option){
        setSelected((prevState)=>({
            display: {...prevState.display, [filterData.displayText]: option},
            request: {...prevState.request, [filterData.filterId]: filterData.options[option]}
        }))
    }

    function renderComponent(typeId){
        switch(typeId){
            case 'multi-select':
                return <MultiSelectFilter filterData={filterData} setSelected={setSelected}/>
            case 'single-select':
                return <SingleSelectFilter filterData={filterData} setSelected={setSelected}/>
            case 'range-select':
                return <RangeSliderFilter filterData={filterData} setSelected={setSelected}/>
            case 'credit-input':
                return <CreditInputFilter filterData={filterData} setSelected={setSelected}/>
            case 'country-input':
                return <CountryInputFilter filterData={filterData} setSelected={setSelected}/>
            default:
                return <p>Error?</p>
        }
    }

    return(
        <article>
            <h2>{filterData.displayText}</h2>
            <div>
                {renderComponent(filterData.type)}
            </div>
        {/*
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
        */}
        </article>
    )
}