#include <fstream>
#include <vector>

using namespace std;

// Constraint: Todos los participantes deben jugar dos veces con cada uno
// de los otros participantes, una como "visitantes" y la otra como "locales".
// (forall i,j | i!=j : (exists only one d,h |: X(i,j,d,h) )
void rule_1(ofstream &file, vector<vector<vector<vector<int>>>> &map, int np, int nd, int nh)
{
	for (int i = 0; i < np; ++i)
	{
		for (int j = 0; j < np; ++j)
		{
			if (i == j)
				continue;

			for (int k = 0; k < nd; ++k)
			{
				for (int l = 0; l < nh; ++l)
				{
					file << map[i][j][k][l] << " ";
				}
			}

			file << "0\n";
		}
	}
}

// Constraint: Un participante puede jugar a lo sumo una vez por día.
// (forall i,j,d,h | i!=j : X(i,j,d,h) => not(exists k,l | : X(i,k,d,l) or X(k,j,d,l) or X(j,k,d,l) or X(k,i,d,l)))
void rule_3(ofstream &file, vector<vector<vector<vector<int>>>> &map, int np, int nd, int nh)
{
	for (int i = 0; i < np; ++i)
	{
		for (int j = 0; j < np; ++j)
		{
			if (i == j)
				continue;

			for (int k = 0; k < nd; ++k)
			{
				for (int l = 0; l < nh; ++l)
				{
					int not_x_ijkl = -map[i][j][k][l];

					for (int _p = 0; _p < np; ++_p)
					{
						for (int q = 0; q < nh; ++q)
						{
							if (q == l)
								continue;

							file << not_x_ijkl << " " << -map[i][_p][k][q] << " 0\n";
							file << not_x_ijkl << " " << -map[_p][j][k][q] << " 0\n";
							file << not_x_ijkl << " " << -map[j][_p][k][q] << " 0\n";
							file << not_x_ijkl << " " << -map[_p][i][k][q] << " 0\n";
						}
					}
				}
			}
		}
	}
}

// Constraint: Un participante no puede jugar de "visitante" en dos días consecutivos,
// ni de "local" dos días seguidos.
// (forall i,j,d,h | i!=j  d<D-1 : X(i,j,d,h) => not(exists k,l | : X(i,k,d+1,l) or X(k,j,d+1,l)))
void rule_4(ofstream &file, vector<vector<vector<vector<int>>>> &map, int np, int nd, int nh)
{
	for (int i = 0; i < np; ++i)
	{
		for (int j = 0; j < np; ++j)
		{
			if (i == j)
				continue;

			for (int k = 0; k < nd - 1; ++k)
			{
				for (int l = 0; l < nh; ++l)
				{
					int not_x_ijkl = -map[i][j][k][l];

					for (int _p = 0; _p < np; ++_p)
					{
						for (int q = 0; q < nh; ++q)
						{
							file << not_x_ijkl << " " << -map[i][_p][k + 1][q] << " 0\n";
							file << not_x_ijkl << " " << -map[_p][j][k + 1][q] << " 0\n";
						}
					}
				}
			}
		}
	}
}