import { Sheet, Typography } from "@mui/joy"

export const Footer = () => {
    return (
        <Sheet sx={{borderTop: '2px solid #f1ebf5', width: '100%', height: '3vh', padding: '30px', textAlign: 'center', backgroundColor: '#f2f2f2', overflow:'hidden'}}>
            <Typography>&copy; 2022 Aiden Mead BSCS Capstone</Typography>
        </Sheet>
    )
}