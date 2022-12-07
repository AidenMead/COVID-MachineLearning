import { Bar, BarChart, Legend, Tooltip, XAxis, YAxis } from 'recharts'
import { Box, Typography } from '@mui/material'


export const RenderBarChart = ({ value, panelIndex, demographic, data }) => {
    return (
        <div hidden={value !== panelIndex} >
            {value === panelIndex && (
                <Box sx={{textAlign:'center'}}>
                <Typography>{demographic.toUpperCase()}</Typography>
                <Box key={panelIndex}>
                    <BarChart width={730} height={250} data={data[demographic]}>
                        <XAxis dataKey='demographic' />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Bar dataKey='hospitalized' fill="#d864d8" />
                        <Bar dataKey='icu' fill="#388dd8" />
                        <Bar dataKey='death' fill="#8884d8" />
                    </BarChart>
                </Box>
                </Box>
            )}
        </div>
    )
}