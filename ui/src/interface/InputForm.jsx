import { Box, Divider, Sheet } from "@mui/joy"
import { Button, MenuItem, Typography, Select, InputLabel, FormControl, styled } from '@mui/material'
import axios from 'axios'
import { useState } from "react"

const StyledFormControl = styled(FormControl)(({theme})=> ({
    width: '250px', 
    display: 'flex', 
    flexDirection: 'column',
    margin: '10px'
}))

export const InputForm = ({ setResults }) => {
    const [ formValues, setFormValues ] = useState({
        sex: '',
        age: '',
        comorbidity:'',
        symptomatic: '',
        currentStatus: ''
    })

    const sendValues = async () => {
        await axios({
            method: 'POST',
            url: '/api/demographics',
            data: formValues
        }).then(resp => {
            setResults(resp.data)
        })
    }

    const handleChange = (e) => {
        setFormValues({
            ...formValues,
            [e.target.name]: e.target.value
        })
    }

    const handleSubmit = () => {
        sendValues()
    }

    return (
        <Box>
            <Typography variant="h5">Patient Demographics</Typography>
            <Divider />
            <Box sx={{ display: 'flex', flexDirection: 'row' }}>
                <Sheet>

                    <StyledFormControl >
                        <InputLabel id='sexInputLabel'>Sex</InputLabel>
                        <Select label="Sex"
                            name='sex'
                            defaultValue={''}
                            onChange={handleChange}>
                            <MenuItem value={'Male'}>Male</MenuItem>
                            <MenuItem value={'Female'}>Female</MenuItem>
                        </Select>
                    </StyledFormControl>
                    <StyledFormControl>
                        <InputLabel id='ageInputLabel'>Age</InputLabel>
                        <Select label="Age"
                            name='age'
                            defaultValue={''}
                            onChange={handleChange}>
                            <MenuItem value={'0-17 years'}>0-17 years</MenuItem>
                            <MenuItem value={'18-49 years'}>18-49 years</MenuItem>
                            <MenuItem value={'50-64 years'}>50-64 years</MenuItem>
                            <MenuItem value={'65+ years'}>65+ years</MenuItem>
                        </Select>
                    </StyledFormControl>
                </Sheet>
                <Sheet>
                    <StyledFormControl >
                        <InputLabel id='comorbidityInputLabel'>Underlying Conditions</InputLabel>
                        <Select label="Underlying Conditions"
                            name='comorbidity'
                            defaultValue={''}
                            onChange={handleChange}>
                            <MenuItem value={'Yes'}>Yes</MenuItem>
                            <MenuItem value={'No'}>No</MenuItem>
                        </Select>
                    </StyledFormControl>
                    <StyledFormControl >
                        <InputLabel id='symtomaticLabel'>Symptom Status</InputLabel>
                        <Select label="Symptom Status"
                            name='symptomatic'
                            defaultValue={''}
                            onChange={handleChange}>
                            <MenuItem value={'Asymtomatic'}>Asymptomatic</MenuItem>
                            <MenuItem value={'Symptomatic'}>Symptomatic</MenuItem>
                        </Select>
                    </StyledFormControl>
                </Sheet>
                <Sheet>
                    <StyledFormControl >
                        <InputLabel id='currentStatusLabel'>COVID Status</InputLabel>
                        <Select label="COVID Status"
                            name='currentStatus'
                            defaultValue={''}
                            onChange={handleChange}>
                            <MenuItem value={'Confirmed Case'}>Laboratory Confirmed Case</MenuItem>
                            <MenuItem value={'Probable Case'}>Probable Case</MenuItem>
                        </Select>
                    </StyledFormControl>
                    <Button sx={{ width: '250px', height: '56px', marginLeft: '10px' }} variant="contained" onClick={handleSubmit}>Predict</Button>
                </Sheet>
            </Box>
        </Box>
    )
}