import 'dotenv';

dotenv.config();

interface ApiUserCoordinates {
	"date_time": "2019-02-12T10:57:36+00:00",
	"latitude": "-18.92406700",
	"longitude": "-48.28214200"

}

const getUserCoordinates = async () => {
  const response = await fetch(`${process.env.BASE_API}/user-coordinates`);
  return await response.json() as Array<UserCoo
}
