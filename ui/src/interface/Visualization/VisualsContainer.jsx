import { Box, Divider, Typography, Tab, Tabs } from "@mui/material"
import { Charts } from "./Charts"
import axios from "axios"
import { useState, useEffect } from "react"
import './Loading.css'

export const VisualsContiner = () => {
    const [ isLoading, setIsLoading ] = useState(true)
    const [ data, setData ] = useState({})
    const [ value, setValue ] = useState(0)
    const [ totals, setTotals ] = useState()

    const getData = async () => {
        await axios.get('/chart-data').then(resp => {
            setData(resp.data.values_arr)
            setTotals(resp.data.total_counts)
            setIsLoading(false)
        })
    }

    useEffect(()=> {
        getData()
    }, [])

    const handleChange = (e, newValue) => {
        setValue(newValue)
    }

    return (
        <Box>
            <Typography variant='h5'>COVID Data and Statistics</Typography>
            <Divider />
            { isLoading ? 
            <Box sx={{ margin: 3 }}>
                <Typography variant='h5' align='center'>Loading...</Typography>
                <Box sx={{border: '4px solid green', borderRadius: 5, width: '200px', height: '10px', margin: '0 auto', position: 'relative'}}>
                    <div class="progress-bar"></div>
                </Box>
            </Box>
            :
            <Box sx={{ padding: 3 }}>
                <Box sx={{ borderBottom: 1, borderColor: 'divider', marginBottom: 4, position: 'sticky', top: '60px', backgroundColor: 'white', zIndex: '9999', width: (document.body.scrollTop === 0 && '100%') }}>
                    <Tabs value={value} onChange={handleChange} centered >
                        {Object.keys(data).map((each, idx) => {
                            return <Tab label={each} key={idx} value={idx} />
                        })}
                    </Tabs>
                </Box>
                {data &&
                    <Box>
                        {Object.keys(data).map((each, idx) => {
                            return (
                                <Charts value={value} demographic={each} key={idx} panelIndex={idx} data={data} totals={totals}/>
                            )
                        })}
                    </Box>

                }
            </Box>
        }
        </Box>
    )
}
