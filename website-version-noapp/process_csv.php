<?php
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['csv'])) {
    $csvFile = $_FILES['csv']['tmp_name'];

    if (file_exists($csvFile)) {
        $boys = [];
        $girls = [];

        $handle = fopen($csvFile, 'r');
        $header = fgetcsv($handle);
        
        // Debug: Output header row
        error_log('CSV Header: ' . implode(', ', $header));

        while (($data = fgetcsv($handle)) !== FALSE) {
            $row = array_combine($header, $data);
            
            // Debug: Output row data
            error_log('CSV Row: ' . json_encode($row));

            $team = $row['Team'];
            $name = $row['FName'] . ' ' . $row['LName'];
            $grade = $row['Grade'];
            $gender = $row['Gender'];

            $formattedRow = [
                'Team' => $team,
                'Name' => $name,
                'Grade' => $grade
            ];

            if ($gender === 'Boys') {
                $boys[] = $formattedRow;
            } else if ($gender === 'Girls') {
                $girls[] = $formattedRow;
            }
        }

        fclose($handle);

        usort($boys, function ($a, $b) {
            return $a['Team'] === $b['Team'] ? strcmp($a['Name'], $b['Name']) : strcmp($a['Team'], $b['Team']);
        });

        usort($girls, function ($a, $b) {
            return $a['Team'] === $b['Team'] ? strcmp($a['Name'], $b['Name']) : strcmp($a['Team'], $b['Team']);
        });

        $boysOutput = fopen('boys.txt', 'w');
        $girlsOutput = fopen('girls.txt', 'w');

        fwrite($boysOutput, "Team\tName\tGrade\n");
        fwrite($girlsOutput, "Team\tName\tGrade\n");

        foreach ($boys as $row) {
            fwrite($boysOutput, implode("\t", $row) . "\n");
        }

        foreach ($girls as $row) {
            fwrite($girlsOutput, implode("\t", $row) . "\n");
        }

        fclose($boysOutput);
        fclose($girlsOutput);

        // Ensure the paths are correct for downloading
        $baseUrl = 'http://' . $_SERVER['HTTP_HOST'] . dirname($_SERVER['REQUEST_URI']) . '/';
        echo json_encode(['success' => true, 'boysUrl' => $baseUrl . 'boys.txt', 'girlsUrl' => $baseUrl . 'girls.txt']);
    } else {
        echo json_encode(['success' => false, 'message' => 'File upload failed.']);
    }
} else {
    echo json_encode(['success' => false, 'message' => 'Invalid request.']);
}
?>
