import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import {
    Row,
    Col,
    Collapse,
    Button,
} from 'antd';

const MovieDetail = () => {
    const baseURL: String = 'http://127.0.0.1:8000/api';
    const navigate = useNavigate();
    const params = useParams();
    const [movieReviews, setMovieReviews] = useState<String[]>([]);

    const handleReturn = (): void => {
        navigate('/');
    }

    useEffect(() => {
        const movieName = params.movieName;

        const fetchMovieReviews = async (): Promise<void> => {
            try {
                const res = await axios.post(baseURL + '/movie_descriptions', {
                    'movie': movieName,
                });

                setMovieReviews(res.data.movie_descriptions);
            } catch (error) {
                console.log(error);
            }
        }

        fetchMovieReviews();
    }, [params.movieName]);

    return (
        <div style={{ minHeight: 1000, background: 'black' }}>
            <Row style={{ padding: 20 }}>
                <Col span={5} offset={1}>
                    <Button type='primary' onClick={handleReturn}>
                        Return
                    </Button>
                </Col>
            </Row>
            <Row>
                <Col span={22} offset={1}>
                    <Collapse defaultActiveKey={[]} style={{ background: 'gray' }} >
                        {
                            movieReviews.map((review, index) => {
                                return (
                                    <Collapse.Panel key={index} header={'Review' + index} style={{ margin: 20 }}>
                                        <div dangerouslySetInnerHTML={{ __html: review as string }} />
                                    </Collapse.Panel>
                                )
                            })
                        }
                    </Collapse>
                </Col>
            </Row>
        </div>
    )
}

export default MovieDetail
