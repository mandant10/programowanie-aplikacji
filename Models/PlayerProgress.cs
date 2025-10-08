namespace MinesweeperAPI.Models;

public class PlayerProgress
{
    public int Id { get; set; }
    public string PlayerName { get; set; } = string.Empty;
    public bool EasyCompleted { get; set; }
    public bool MediumCompleted { get; set; }
    public bool HardCompleted { get; set; }
    public string CurrentTexture { get; set; } = "default"; // "default", "bronze", "silver", "gold"
}
