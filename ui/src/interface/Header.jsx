import {  } from "@mui/joy"
import { AppBar, Typography } from "@mui/material"

export const Header = () => {
    return (
        <AppBar sx={{ height: '60px', display: 'flex', flexDirection: 'column', justifyContent: 'center', padding: 2}}>
            <Typography variant='h5'>COVID Case Severity Prediction</Typography>
        </AppBar>
    )
}