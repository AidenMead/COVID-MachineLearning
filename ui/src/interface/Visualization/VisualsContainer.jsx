import { Box, Divider, Typography, Tab, Tabs } from "@mui/material"
import { RenderBarChart } from "./BarChart"
import axios from "axios"
import { useState, useEffect } from "react"
import { CorrelationTable } from "./CorrelationTable"

export const VisualsContiner = () => {
    const [ data, setData ] = useState({})
    const [ value, setValue ] = useState(0)

    const getData = async () => {
        await axios.get('/chart-data').then(resp => {
            setData(resp.data.values_arr)
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
            <Box sx={{ padding: 3 }}>
                <Box sx={{ borderBottom: 1, borderColor: 'divider', marginBottom: 4}}>
                    <Tabs value={value} onChange={handleChange}>
                        {Object.keys(data).map((each, idx) => {
                            return <Tab label={each} key={idx} value={idx} />
                        })}
                    </Tabs>
                </Box>
                {data &&
                    <Box>
                        {Object.keys(data).map((each, idx) => {
                            return (
                                <RenderBarChart value={value} demographic={each} key={idx} panelIndex={idx} data={data} />
                            )
                        })}
                        <Box>
                            <CorrelationTable data={data} />
                        </Box>
                    </Box>

                }
            </Box>
        </Box>
    )
}
