export const Results = ({prediction}) => {
    return(
        <Box>
            <Typography>Probability of hospitalization: {prediction.hospitalization}</Typography>
            <Typography>Probability of ICU need: {prediction.icu}</Typography>
        </Box>
    )
}