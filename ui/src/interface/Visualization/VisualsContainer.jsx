import { Box, Divider, Typography, Tab, Tabs } from "@mui/material"
import { Charts } from "./Charts"
import axios from "axios"
import { useState, useEffect } from "react"
import { useRef } from "react"

export const VisualsContiner = () => {
    const [ data, setData ] = useState({})
    const [ value, setValue ] = useState(0)
    const [ totals, setTotals ] = useState()

    const ref = useRef()

    const getData = async () => {
        await axios.get('/chart-data').then(resp => {
            setData(resp.data.values_arr)
            setTotals(resp.data.total_counts)
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
        </Box>
    )
}
