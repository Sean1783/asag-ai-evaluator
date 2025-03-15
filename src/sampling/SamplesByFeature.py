import SamplingStrategy

class SamplesByFeature(SamplingStrategy):
    def sample(self, dataframe, feature, n: int):
        # feature_list = dataframe.columns.tolist()
        sample_list = []
        # for feature in feature_list:
        samples = dataframe.groupby(feature).head(n)
        sample_list.append(samples)
        return sample_list
