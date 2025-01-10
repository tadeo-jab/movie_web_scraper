import React from "react";

export default function SelectedBar({selected, setSelected}){

    return(
        <article>
            {
            <div>
                {selected.display != {} ? (
                    Object.entries(selected.display).map(([filter, option], k)=>(
                    <p key={k}>{`${filter}: ${option}`}</p>
                ))) : null}
            </div>
            }
        </article>
    )
}