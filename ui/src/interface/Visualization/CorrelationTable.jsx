import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from "@mui/material"

export const CorrelationTable = ({ data }) => {
    return (
        <TableContainer>
            <Table>
                <TableHead>
                    <TableRow>
                        <TableCell>Demographic Correlation</TableCell>
                        <TableCell>Hospitalized</TableCell>
                        <TableCell>ICU Admitted</TableCell>
                        <TableCell>Deceased</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {Object.keys(data).map((demo, index) => {
                        return(
                        <TableRow>
                            <TableCell>{demo.toUpperCase()}</TableCell>
                            {data[demo].map((valueObj, index)=> {
                                return (
                                    <TableRow>
                                        <TableCell>{valueObj.demographic}</TableCell>
                                        <TableCell>{valueObj.hospitalized}</TableCell>
                                        <TableCell>{valueObj.icu}</TableCell>
                                        <TableCell>{valueObj.death}</TableCell>
                                    </TableRow>   
                                )
                            })}
                        </TableRow>
                        )
                    })}
                </TableBody>
            </Table>
        </TableContainer>
    )
}