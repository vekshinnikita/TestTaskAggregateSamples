
from datetime import datetime
from dateutil.relativedelta import relativedelta
from bisect import bisect_left
from app.database.models.sample import Sample
from app.schemas.sample import SampleAggregateRequest, SampleAggregateTypeEnum 


class SampleService:
    @staticmethod
    async def aggregate_by_period(request: SampleAggregateRequest):
        samples = await Sample.filter_by_date_range(request.start_date, request.end_date)

        aggregate_dict = SampleService._generate_aggregate_dict(request)

        times = [datetime.fromisoformat(el) for el in aggregate_dict['labels']]

        for sample in samples:
            index = SampleService._binary_search_in_aggregate_labels(times, sample.timestamp)
            aggregate_dict['dataset'][index] += sample.value
            
        return aggregate_dict
    
    @staticmethod
    def _binary_search_in_aggregate_labels(times: list[datetime], date: datetime,):
        index = bisect_left(times, date)
        if (len(times) - 1 < index or times[index] != date):
            index -= 1
        return index

    @staticmethod
    def _generate_aggregate_dict(request: SampleAggregateRequest):
        start_date = SampleService._extract_from_date(request.start_date, request.type)
        end_date = SampleService._extract_from_date(request.end_date, request.type)

        temp_date = start_date
        delta_dict = {
            SampleAggregateTypeEnum.HOUR: relativedelta(hours=1),
            SampleAggregateTypeEnum.DAY: relativedelta(days=1),
            SampleAggregateTypeEnum.MONTH: relativedelta(months=1)
        }

        aggregate_dict = {
            "dataset": [],
            "labels": []
        }

        while temp_date != end_date:
            aggregate_dict["dataset"].append(0)
            aggregate_dict["labels"].append(temp_date.isoformat())

            temp_date += delta_dict[request.type]
        
        aggregate_dict["dataset"].append(0)
        aggregate_dict["labels"].append(temp_date.isoformat())

        return aggregate_dict

    @staticmethod
    def _extract_from_date(date: datetime, type: SampleAggregateTypeEnum):
        arr = [date.year, date.month]
        match type:
            case SampleAggregateTypeEnum.DAY:
                arr.append(date.day)
            case SampleAggregateTypeEnum.HOUR:
                arr.extend([date.day, date.hour])
            case SampleAggregateTypeEnum.MONTH:
                arr.append(1)
        
        return datetime(*arr)# type: ignore


