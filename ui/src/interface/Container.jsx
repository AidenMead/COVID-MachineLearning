import { Sheet } from '@mui/joy'
import { Paper } from '@mui/material'
import { useState } from 'react'
import { InputForm } from './InputForm'
import { ResultsContainer } from './ResultsContainer'
import { VisualsContiner } from './Visualization/VisualsContainer'

export const MainContainer = () => {
    const [ results, setResults ] = useState()

    return (
        <Sheet sx={{width: '100vw', display: 'flex', flexDirection: 'column', alignItems:'center', marginTop: '60px', backgroundColor: '#f2f2f2', minHeight: '85vh'}}>
            <Paper elevation={4} sx={{padding: 3, margin: 3, width: '858px'}}>
                <InputForm setResults={setResults} />
                {results && <ResultsContainer prediction={results} />}
            </Paper>
            <Paper elevation={4} sx={{padding: 3, margin: 3, width: '858px'}}>
                <VisualsContiner/>
            </Paper>
        </Sheet>
    )
}