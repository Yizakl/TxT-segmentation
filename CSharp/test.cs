using System;
using System.IO;
using System.Text;
using System.Windows.Forms;

public class FileSplitterForm : Form
{
    private Button btnChooseFile;
    private Button btnSplit;
    private TextBox txtParts;
    private OpenFileDialog openFileDialog;
    private ProgressBar progressBar;
    private string filePath;

    public FileSplitterForm()
    {
        // 初始化控件
        btnChooseFile = new Button { Text = "Choose File", Width = 100, Height = 30 };
        btnChooseFile.Click += BtnChooseFile_Click;
        btnChooseFile.Location = new System.Drawing.Point(10, 10);

        txtParts = new TextBox { Width = 100, Location = new System.Drawing.Point(10, 50) };

        btnSplit = new Button { Text = "Split File", Width = 100, Height = 30 };
        btnSplit.Click += BtnSplit_Click;
        btnSplit.Location = new System.Drawing.Point(10, 90);

        progressBar = new ProgressBar { Width = 300, Height = 30, Location = new System.Drawing.Point(10, 130) };

        openFileDialog = new OpenFileDialog();
        openFileDialog.Filter = "Text files (*.txt)|*.txt|All files (*.*)|*.*";

        Controls.Add(btnChooseFile);
        Controls.Add(txtParts);
        Controls.Add(btnSplit);
        Controls.Add(progressBar);
    }

    // 选择文件按钮点击事件
    private void BtnChooseFile_Click(object sender, EventArgs e)
    {
        if (openFileDialog.ShowDialog() == DialogResult.OK)
        {
            filePath = openFileDialog.FileName;
            MessageBox.Show($"选择的文件路径: {filePath}");
        }
    }

    // 拆分文件按钮点击事件
    private void BtnSplit_Click(object sender, EventArgs e)
    {
        if (string.IsNullOrEmpty(filePath))
        {
            MessageBox.Show("请先选择文件！");
            return;
        }

        int numParts;
        if (!int.TryParse(txtParts.Text, out numParts) || numParts <= 0)
        {
            MessageBox.Show("请输入有效的拆分份数（正整数）。");
            return;
        }

        try
        {
            SplitFile(filePath, numParts);
            MessageBox.Show("文件拆分成功！");
        }
        catch (Exception ex)
        {
            MessageBox.Show($"错误: {ex.Message}");
        }
    }

    // 文件拆分逻辑
    private void SplitFile(string filePath, int numParts)
    {
        string[] lines = File.ReadAllLines(filePath, Encoding.UTF8);
        int totalLines = lines.Length;
        int partSize = totalLines / numParts;
        int remainder = totalLines % numParts;

        string directory = Path.GetDirectoryName(filePath);
        string baseFileName = Path.GetFileNameWithoutExtension(filePath);

        int start = 0;
        for (int i = 0; i < numParts; i++)
        {
            int end = start + partSize + (i < remainder ? 1 : 0);
            string outputFile = Path.Combine(directory, $"{baseFileName}_part{i + 1}.txt");

            // 写入文件
            File.WriteAllLines(outputFile, lines[start..end], Encoding.UTF8);

            // 更新进度条
            start = end;
            progressBar.Value = (int)((float)(i + 1) / numParts * 100);
        }
    }

    // 程序入口
    public static void Main()
    {
        Application.EnableVisualStyles();
        Application.SetCompatibleTextRenderingDefault(false);
        Application.Run(new FileSplitterForm());
    }
}
