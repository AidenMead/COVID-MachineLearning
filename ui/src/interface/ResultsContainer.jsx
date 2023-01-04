import { Box } from "@mui/joy"
import { Typography, Divider } from "@mui/material"

export const ResultsContainer = ({prediction}) => {
    
    const handleColor = (value) => {
        let style = {
            padding: 2, 
            margin: 3, 
            width: '200px',
            borderRadius: '5px',
            backgroundColor: ''
        }

        if (value >= 0.15) {
            style['border'] = '4px solid #ff0000'
            return style
        } else if (value < 0.15 && value >= 0.05) {
            style['border'] = '4px solid #e6b800'
            return style
        } else if (value < 0.05){
            style['border'] = '4px solid #009933'
            return style
        }
    }

    const convertToPercent = (value) => {
        return (value*100).toFixed(2)
    }

    return(
        <Box sx={{maxWidth: '810px'}}>
            <Divider sx={{margin: 4}}/>
            <Typography variant='h5'>Case Severity Risk</Typography>
        <Box sx={{display: 'flex', flexDirection: 'row', textAlign: 'center'}}>
            
            <Box sx={handleColor(prediction['hosp'])} >
                <Typography>
                    Hospitalization
                </Typography>
                <Typography sx={{fontSize: '2'}}>
                    {convertToPercent(prediction['hosp'])}%
                </Typography>
                
            </Box>
            <Box sx={handleColor(prediction['icu'])} >
                <Typography>
                    ICU
                </Typography>
                <Typography fontWeight='lg' fontSize='xl3'>
                    {convertToPercent(prediction['icu'])}%
                </Typography>
                
            </Box>
            <Box sx={handleColor(prediction['death'])} >
                <Typography>
                    Death
                </Typography>
                <Typography fontWeight='lg' fontSize='xl3'>
                    {convertToPercent(prediction['death'])}%
                </Typography>
                
            </Box>
        </Box>
        </Box>
    )
}