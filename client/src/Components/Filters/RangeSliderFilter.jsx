import React, { useEffect, useRef, useState } from "react";
import MultiRangeSlider from "multi-range-slider-react"
import '../../Styles/RangeSliderFilter.css'

export default function RangeSliderFilter({filterData, selected, setSelected}){
    const filName = filterData.displayText
    const filId = filterData.filterId
    const filOptions = filterData.options

    const sliderRef = useRef()
    const minRef = useRef(filOptions.min)
    const maxRef = useRef(filOptions.max)

    function sliderHandler(e){
        minRef.current = e.minValue;
        maxRef.current = e.maxValue;
    };

    function updateOptions(event){
        let displayValues = {} 
        let requestValues = {} 

        if((filOptions.modifier === null) || ((filOptions.modifier === 'plus') && (maxRef.current !== filOptions.max))){
            displayValues = {min: minRef.current, max: maxRef.current }
            requestValues = {min: minRef.current, max: maxRef.current }
        }
        else if((filOptions.modifier === 'plus') && (maxRef.current === filOptions.max)){
            displayValues = {min: minRef.current, max: `${maxRef.current}+`  }
            requestValues = {min: minRef.current, max: filOptions.plus}
        }
        else if(filOptions.modifier === 'date'){
            displayValues = {min: minRef.current, max: maxRef.current }
            requestValues = {start: `${minRef.current}-01-01`, end: `${maxRef.current}-12-31` }
        }

        setSelected((prevState)=>({
            display: {...prevState.display, [filName]: `${displayValues.min} to ${displayValues.max}`},
            request: {...prevState.request, [filId]: requestValues}
        }))
    }


    function resetSlider(){
        setSelected((prevState)=>{
            const newState = {...prevState}

            delete newState.display[filName]
            delete newState.request[filId]

            return newState
        })
    }

    useEffect(()=>{
        if(sliderRef.current){
            sliderRef.current.addEventListener("mouseup", updateOptions)
        }
    }, [])

    return(
        <article>
            <MultiRangeSlider
                min={filOptions.min}
                max={filOptions.max}
                step={filOptions.step}
                minValue={filOptions.min}
                maxValue={filOptions.max}
                barInnerColor= "rgb(19, 209, 187)"
                onInput={(e) => {
                    sliderHandler(e);
                }}
                ruler={false}
                label={false}
                stepOnly={true}
                ref={sliderRef}
            />
            <div>
                <span>{filOptions.min} </span>
                <span>{filOptions.max} </span>
            </div>
            <button onClick={()=>resetSlider()}>Deselect</button>
        </article>
    )
}