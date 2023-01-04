import { Bar, BarChart, Legend, Tooltip, XAxis, YAxis, LineChart, Line, CartesianGrid, Cell, Pie, PieChart } from 'recharts'
import { Box, Typography } from '@mui/material'
import { useState } from 'react'
import { useEffect } from 'react'


export const Charts = ({ value, panelIndex, demographic, data, totals }) => {

    const [ pieData, setPieData ] = useState()
    const [ lineData, setLineData ] = useState()

    useEffect(() => {
        setPieData([calcPieDataInner(), calcPieDataOuter()])
        setLineData(calcLineDistribution())
    }, [])

    const COLORS = {
    INNER: ['#FF8042','#0088FE', '#FFBB28', '#00C49F'],
    OUTER: ['#5b3ff0', '#7f30be', '#789878', '#97aec2']
    }

    const calcPieDataInner = () => {
        // Inner pie chart will show: # Non-Event COVID patients (total minus all hosp, icu, and death combined), how many hospitalized, icu, and death
        const nonEvent = (totals.all - totals.hospitalized - totals.icu - totals.death)
        let eventSplit = [
            {name: "Mild", value: nonEvent},
            {name: "Hospitalized", value: totals.hospitalized},
            {name: "ICU", value: totals.icu},
            {name: "Death", value: totals.death},
        ]
        eventSplit.sort((objA, objB)=> {
            return objA.name.toLowerCase().localeCompare(objB.name.toLowerCase())
        })
        return eventSplit
    }

    const calcPieDataOuter = () => {
        // Outer pie chart will show demographics splits - how many have and don't have confirmed covid of each
        let dynamic = []
        data[demographic].forEach(demo => {
            dynamic.push({name: `Mild - ${demo.demographic}`, value: (demo.total_count - demo.hospitalized - demo.icu - demo.death)},)
            dynamic.push({name: `Hospitalized - ${demo['demographic']}`, value: (demo.hospitalized)},)
            dynamic.push({name: `ICU - ${demo['demographic']}`, value: (demo.icu)},)
            dynamic.push({name: `Death - ${demo['demographic']}`, value: (demo.death)},)
        })
        dynamic.sort((objA, objB)=> {
            return objA.name.toLowerCase().localeCompare(objB.name.toLowerCase())
        })
        return dynamic
    }


    const calcLineDistribution = () => {
        const events = ['mild', 'hospitalized', 'icu', 'death']
        const percentages = []
        data['ages'].forEach((demo)=>{
            const list = {}
            list['demographic'] = demo['demographic']
            events.forEach(event => {
                list[event] = (demo[event]*100)/demo['total_count']
            })
            percentages.push(list)
        })
        return percentages
    }

    return (
        <div hidden={value !== panelIndex} >
            {value === panelIndex && (
                <Box sx={{ textAlign: 'center' }}>
                    <Box key={panelIndex} sx={{ boxShadow: 3, padding: 3, borderRadius: 3, margin: 3 }}>
                    <Typography variant="h4">Distribution of Demographics - {demographic.toUpperCase()}</Typography>
                        <BarChart width={730} height={450} data={data[demographic]} margin={{top: 20}} >
                            <XAxis dataKey='demographic' />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Bar dataKey='hospitalized' fill="#ffcc66" label={{ position: 'top' }} />
                            <Bar dataKey='icu' fill="#ff6600" label={{ position: 'top' }} />
                            <Bar dataKey='death' fill="#990000" label={{ position: 'top' }} />
                        </BarChart>
                    </Box>
                    
                    {pieData &&
                        <Box sx={{ boxShadow: 3, padding: 3, borderRadius: 3, margin: 3 }}>
                            <Typography variant="h4">Distribution of Data - {demographic.toUpperCase()}</Typography>
                            <PieChart width={730} height={450} >
                                <Tooltip />
                                <Legend />
                                <Pie data={pieData[0]} label={totals.name} dataKey="value" nameKey="name" outerRadius={100} >
                                    {pieData[0].map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS.INNER[index % COLORS.INNER.length]} />
                                    ))}
                                </Pie>
                                <Pie data={pieData[1]} label={totals.name} dataKey="value" nameKey="name" innerRadius={100} outerRadius={150} >
                                    {pieData[1].map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS.OUTER[index%4]} />
                                    ))}
                                </Pie>
                            </PieChart>
                        </Box>
                    }
                    <Box sx={{ boxShadow: 3, padding: 3, borderRadius: 3, margin: 3 }}>
                        <Typography variant="h4">Percentage Distribution Across Ages</Typography>
                        <LineChart width={730} height={450} data={lineData}
                            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
                            isAni>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="demographic" />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Line type="monotone" dataKey="mild" stroke="#00b300" />
                            <Line type="monotone" dataKey="hospitalized" stroke="#8884d8" />
                            <Line type="monotone" dataKey="icu" stroke="#82ca9d" />
                            <Line type="monotone" dataKey="death" stroke="#a2ca2d" />
                        </LineChart>
                    </Box>
                </Box>
            )}
        </div>
    )
}