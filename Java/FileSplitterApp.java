import javax.swing.*;
import java.awt.*;
import java.io.*;
import java.nio.charset.StandardCharsets;

public class FileSplitterApp extends JFrame {
    private JButton chooseFileButton, splitButton;
    private JTextField partsField;
    private JFileChooser fileChooser;
    private JProgressBar progressBar;

    public FileSplitterApp() {
        setTitle("File Splitter");
        setSize(400, 250);
        setLayout(new FlowLayout());

        chooseFileButton = new JButton("Choose File");
        chooseFileButton.addActionListener(e -> chooseFile());
        add(chooseFileButton);

        partsField = new JTextField(10);
        add(partsField);

        splitButton = new JButton("Split File");
        splitButton.addActionListener(e -> splitFile());
        add(splitButton);

        progressBar = new JProgressBar(0, 100);
        progressBar.setStringPainted(true);
        add(progressBar);

        fileChooser = new JFileChooser();
        fileChooser.setFileFilter(new javax.swing.filechooser.FileNameExtensionFilter("Text Files", "txt"));

        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }

    private void chooseFile() {
        int returnValue = fileChooser.showOpenDialog(this);
        if (returnValue == JFileChooser.APPROVE_OPTION) {
            File selectedFile = fileChooser.getSelectedFile();
            // Handle file selection
        }
    }

    private void splitFile() {
        try {
            String filePath = fileChooser.getSelectedFile().getAbsolutePath();
            int numParts = Integer.parseInt(partsField.getText());
            splitFileIntoParts(filePath, numParts);
            JOptionPane.showMessageDialog(this, "File Split Successfully");
        } catch (Exception e) {
            JOptionPane.showMessageDialog(this, "Error: " + e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void splitFileIntoParts(String filePath, int numParts) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(filePath), StandardCharsets.UTF_8));
        String[] lines = reader.lines().toArray(String[]::new);
        reader.close();

        int totalLines = lines.length;
        int partSize = totalLines / numParts;
        int remainder = totalLines % numParts;

        String directory = new File(filePath).getParent();
        String baseFileName = new File(filePath).getName();

        int start = 0;
        for (int i = 0; i < numParts; i++) {
            int end = start + partSize + (i < remainder ? 1 : 0);
            String outputFile = directory + "/" + baseFileName + "_part" + (i + 1) + ".txt";
            try (BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(outputFile), StandardCharsets.UTF_8))) {
                for (int j = start; j < end; j++) {
                    writer.write(lines[j]);
                    writer.newLine();
                }
            }
            start = end;
            progressBar.setValue((int) ((float) (i + 1) / numParts * 100));
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            FileSplitterApp app = new FileSplitterApp();
            app.setVisible(true);
        });
    }
}
