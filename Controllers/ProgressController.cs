using Microsoft.AspNetCore.Mvc;
using MinesweeperAPI.Models;
using MinesweeperAPI.Services;

namespace MinesweeperAPI.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ProgressController : ControllerBase
{
    private readonly IGameService _gameService;

    public ProgressController(IGameService gameService)
    {
        _gameService = gameService;
    }

    /// <summary>
    /// Pobierz postęp gracza
    /// </summary>
    [HttpGet("{playerName}")]
    public async Task<ActionResult<PlayerProgress>> GetProgress(string playerName)
    {
        if (string.IsNullOrWhiteSpace(playerName))
        {
            return BadRequest("PlayerName jest wymagane");
        }

        var progress = await _gameService.GetPlayerProgressAsync(playerName);
        return Ok(progress);
    }

    /// <summary>
    /// Pobierz nagrody gracza
    /// </summary>
    [HttpGet("{playerName}/rewards")]
    public async Task<ActionResult<List<Reward>>> GetRewards(string playerName)
    {
        if (string.IsNullOrWhiteSpace(playerName))
        {
            return BadRequest("PlayerName jest wymagane");
        }

        var rewards = await _gameService.GetRewardsAsync(playerName);
        return Ok(rewards);
    }
}
