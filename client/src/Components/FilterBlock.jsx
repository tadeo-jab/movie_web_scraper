import React from "react";
import MultiSelectFilter from "./Filters/MultiSelectFilter.jsx";
import SingleSelectFilter from "./Filters/SingleSelectFilter.jsx";
import RangeSliderFilter from "./Filters/RangeSliderFilter.jsx";
import CreditInputFilter from "./Filters/CreditInputFilter.jsx";
import CountryInputFilter from "./Filters/CountryInputFilter.jsx";

export default function FilterBlock({filterData, selected, setSelected }){

    //According to each filters' needs, a different type is rendered.

    function renderComponent(typeId){
        switch(typeId){
            case 'multi-select':
                return <MultiSelectFilter filterData={filterData} selected={selected} setSelected={setSelected}/>
            case 'single-select':
                return <SingleSelectFilter filterData={filterData} selected={selected} setSelected={setSelected}/>
            case 'range-select':
                return <RangeSliderFilter filterData={filterData} selected={selected} setSelected={setSelected}/>
            case 'credit-input':
                return <CreditInputFilter filterData={filterData} selected={selected} setSelected={setSelected}/>
            case 'country-input':
                return <CountryInputFilter filterData={filterData} selected={selected} setSelected={setSelected}/>
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
        </article>
    )
}