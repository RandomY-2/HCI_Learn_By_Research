import React from 'react';
import { useParams } from 'react-router-dom';

const MovieDetail = () => {
    const params = useParams();
    const movieName = params.movieName;

    return (
        <div>

        </div>
    )
}

export default MovieDetail
