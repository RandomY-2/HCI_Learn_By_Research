import React, { useState } from 'react';
import './App.css';
import {
    Row,
    Col,
    Input,
    Button,
    Typography,
} from 'antd';
import axios from 'axios';
import { useNavigate } from 'react-router';

const App = () => {
    let navigate = useNavigate();
    const baseURL: String = 'http://127.0.0.1:8000/api';
    const [movieName, setMovieName] = useState<String>("");
    const [movieRecommendations, setMovieRecommendations] = useState<String[]>([]);
    const [selectedMovie, setSelectedMovie] = useState<String>("");

    const handleMovieSearch = async (): Promise<void> => {
        try {
            const res = await axios.post(baseURL + '/movie_suggestions', {
                'movie': movieName
            });
            setMovieRecommendations(res.data.recommended_movies);
        } catch (error) {
            alert(error);
        }
    }

    const handleMovieClick = (index: number): void => {
        navigate(`/movie/${movieRecommendations[index]}`);
    }

    return (
        <div className='app-background'>
            <Row style={{ paddingTop: 40 }}>
                <Col span={12} offset={6}>
                    <Input
                        placeholder='Enter a movie you like to see recommendations'
                        onChange={(e) => setMovieName(e.target.value)}
                    />
                </Col>
            </Row>

            <Row style={{ marginTop: 40, marginBottom: 70 }}>
                <Col span={5} offset={10}>
                    <Button type='primary' onClick={handleMovieSearch}>
                        Get Recommendations
                    </Button>
                </Col>
            </Row>

            {
                movieRecommendations.map((movie: String, i: number) => {
                    return (
                        <Row style={{ marginTop: 10 }} key={movie as React.Key}>
                            <Col span={10} offset={10}>
                                <Typography.Title
                                    level={5}
                                    style={{ color: 'white', cursor: 'pointer' }}
                                    onClick={() => handleMovieClick(i)}
                                >
                                    {movie}
                                </Typography.Title>
                            </Col>
                        </Row>
                    )
                })
            }
        </div>
    )
}

export default App
