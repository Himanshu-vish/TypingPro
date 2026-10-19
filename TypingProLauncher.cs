using System;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Windows.Forms;

sealed class SplashForm : Form {
    Timer poll = new Timer(); Timer startDelay = new Timer(); Process child; string readyFile; Label status;
    public SplashForm() {
        SetStyle(ControlStyles.AllPaintingInWmPaint | ControlStyles.UserPaint | ControlStyles.OptimizedDoubleBuffer, true);
        DoubleBuffered = true;
        UpdateStyles();
        Text="TypingPro"; FormBorderStyle=FormBorderStyle.None; StartPosition=FormStartPosition.CenterScreen;
        ClientSize=new Size(900,540); BackColor=Color.FromArgb(238,246,255); TopMost=true; ShowInTaskbar=false;
        Panel card=new Panel(){Location=new Point(18,18),Size=new Size(864,504),BackColor=Color.White}; Controls.Add(card);
        L(card,"Version 1.0.0",9,FontStyle.Regular,Color.FromArgb(88,113,141),720,15,120,25);
        L(card,"TP",32,FontStyle.Bold,Color.FromArgb(22,132,248),365,45,135,105);
        L(card,"TypingPro",36,FontStyle.Bold,Color.FromArgb(6,26,72),180,145,505,70);
        L(card,"P R A C T I C E   •   T Y P E   •   I M P R O V E",10,FontStyle.Bold,Color.FromArgb(88,115,146),120,210,625,28);
        ProgressBar pb=new ProgressBar(){Location=new Point(220,265),Size=new Size(425,13),Style=ProgressBarStyle.Marquee,MarqueeAnimationSpeed=25}; card.Controls.Add(pb);
        status=L(card,"Preparing your typing workspace...",10,FontStyle.Regular,Color.FromArgb(41,76,115),180,287,505,30);
        string[] a={"⚡  Improve Typing Speed","◎  Build Accuracy","▥  Track Progress","▤  Learn Step by Step"};
        for(int i=0;i<4;i++) L(card,a[i],9,FontStyle.Bold,Color.FromArgb(11,33,72),58+i*194,340,180,55);
        L(card,"“ Small Steps Create Big Results ”",13,FontStyle.Italic,Color.FromArgb(23,58,104),190,410,485,35);
        L(card,"T Y P E   T O D A Y   F O R   A   B E T T E R   T O M O R R O W",8,FontStyle.Bold,Color.FromArgb(38,124,205),120,465,625,25);
        Shown += delegate { Refresh(); startDelay.Start(); };
        startDelay.Interval=150;
        startDelay.Tick += delegate { startDelay.Stop(); BeginInvoke((MethodInvoker)StartMain); };
        poll.Interval=100; poll.Tick+=PollReady;
    }
    Label L(Control p,string t,float z,FontStyle fs,Color c,int x,int y,int w,int h) { Label l=new Label(){Text=t,Font=new Font("Segoe UI",z,fs),ForeColor=c,Location=new Point(x,y),Size=new Size(w,h),TextAlign=ContentAlignment.MiddleCenter}; p.Controls.Add(l); return l; }
    string FindExe(){ string b=AppDomain.CurrentDomain.BaseDirectory; string x=Path.Combine(b,"TypingPro.exe"); if(File.Exists(x))return x; x=Path.Combine(b,"TypingPro","TypingPro.exe"); return File.Exists(x)?x:null; }
    void StartMain(){ try { string exe=FindExe(); if(exe==null) throw new FileNotFoundException("TypingPro.exe not found."); readyFile=Path.Combine(Path.GetTempPath(),"TypingProReady_"+Process.GetCurrentProcess().Id+".flag"); try{File.Delete(readyFile);}catch{} ProcessStartInfo psi=new ProcessStartInfo(exe,"--launcher-mode --ready-file=\""+readyFile+"\""); psi.WorkingDirectory=Path.GetDirectoryName(exe); psi.UseShellExecute=false; child=Process.Start(psi); status.Text="Loading TypingPro..."; poll.Start(); } catch(Exception ex){MessageBox.Show(ex.Message,"TypingPro",MessageBoxButtons.OK,MessageBoxIcon.Error);Close();} }
    void PollReady(object s,EventArgs e){ if(File.Exists(readyFile)){poll.Stop();try{File.Delete(readyFile);}catch{}Close();return;} if(child!=null && child.HasExited){poll.Stop();MessageBox.Show("TypingPro closed before startup completed.","TypingPro");Close();} }
}
static class Program { [STAThread] static void Main(){ Application.EnableVisualStyles(); Application.SetCompatibleTextRenderingDefault(false); Application.Run(new SplashForm()); } }
