import React, { useEffect, useRef, useState } from "react";
import "../Styles/MovieDisplay.css"

export default function SelectedBar({movieList, setMoviesData}){

    const [foundCheck, setFoundCheck] = useState(true)
    const [currentMovie, setCurrentMovie] = useState({})
    const movieCount = useRef(0)
    const movieBlock = (
        <div>
            <div>
                <img src={currentMovie.image} alt={currentMovie.id} className="movie-img"/>
            </div>
            <div>
                <h2>{currentMovie.title}</h2>
                <div>
                    <p>{currentMovie.year}</p>
                    <p>{currentMovie.rating}</p>
                    <p>{currentMovie.genres}</p>
                </div>
                <p>{currentMovie.plot}</p>
            </div>
        </div>
    )


    //If there are no movies after the current one, the "Next" button is hidden.
    
    function displayMovie(){
        if(movieList.length === movieCount.current + 1){
            return(
                <div>
                    {movieBlock}
                </div>
            )
        }
        else{
            return(
                <div>
                    {movieBlock}
                    <button onClick={()=>nextMovie()}>Next Movie</button>
                </div>
            )
        }
    }

    function nextMovie(){
        movieCount.current += 1
        setCurrentMovie(movieList[movieCount.current])
    }

    useEffect(()=>{
        if (movieList.length === 0){
            setFoundCheck(false)
        }
        else{
            setCurrentMovie(movieList[0])
        }
    }, [])

    

    return(
        <article>

            <section>
                {!foundCheck ? (
                    <section> 
                        <h3>No movies fit the criteria</h3>
                    </section>                   
                ):(
                    <section>
                        {displayMovie()}
                    </section>
                )}
            </section>
            
            <button onClick={()=>setMoviesData(null)}> Search Again </button>
        </article>
    )
}